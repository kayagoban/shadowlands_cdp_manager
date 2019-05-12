from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

#import random, string
#from datetime import datetime, timedelta

from shadowlands.credstick import DeriveCredstickAddressError
from decimal import Decimal
from shadowlands.contract import ContractConfigError
from shadowlands.tui.debug import debug
import pdb
import requests
import threading

#from ens_manager.contracts.ens_resolver import EnsResolver
#from ens_manager.contracts.ens_auction import EnsAuction
#from ens_manager.contracts.ens_registry import EnsRegistry
#from ens_manager.contracts.ens_reverse_resolver import EnsReverseResolver

#from ens_manager.status_frame import ENSStatusFrame
from cdp_manager.contracts.sai_pip import SaiPip
from cdp_manager.contracts.sai_pep import SaiPep
from cdp_manager.contracts.sai_pit import SaiPit
from cdp_manager.contracts.sai_top import SaiTop
from cdp_manager.contracts.sai_sin import SaiSin
from cdp_manager.contracts.sai_mom import SaiMom
from cdp_manager.contracts.sai_dad import SaiDad
from cdp_manager.contracts.sai_tub import SaiTub
from cdp_manager.contracts.sai_vox import SaiVox
from cdp_manager.contracts.sai_proxy import SaiProxy
from cdp_manager.contracts.ds_proxy import DsProxy
from cdp_manager.contracts.ds_proxy_factory import DsProxyFactory
from cdp_manager.contracts.maker_otc import MakerOtc
from cdp_manager.contracts.oasis_proxy import OasisProxy
from cdp_manager.contracts.proxy_registry import ProxyRegistry
from cdp_manager.contracts.dai import Dai
from cdp_manager.contracts.mkr import Mkr
from cdp_manager.contracts.peth import Peth

from cdp_manager.cdp_status_frame import CDPStatusFrame
from cdp_manager.open_cdp_frame import OpenCDPFrame
from cdp_manager.cup_id_prompt_frame import CupIDPromptFrame

from cached_property import cached_property


class Dapp(SLDapp):

    RAY = Decimal(10 ** 27)
    WAD = Decimal(10 ** 18)

    # It's a maxed out uint256
    MAX_WEI = (2 ** 256) - 1 
    #'0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    #debug(); pdb.set_trace()

    def initialize(self):
        if self.node.network_name not in ["MainNet", "Kovan"]:
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet and Kovan")
            return
       
        self.show_wait_frame("Querying Maker's Web API for CDP ID...")

        self.cup_id = None
        threading.Thread(target=self._open_cdp_worker).start()


    def _open_cdp_worker(self):
        self.tub = SaiTub(self.node)
        self.vox = SaiVox(self.node)
        self.dai = Dai(self.node)
        self.mkr = Mkr(self.node)
        self.pip = SaiPip(self.node)
        self.pep = SaiPep(self.node)
        self.peth = Peth(self.node) 
        self.proxy_registry = ProxyRegistry(self.node)
        self.sai_proxy = SaiProxy(self.node)
        self.erc20_contract = { 'DAI': self.dai, 'PETH': self.peth }

        try:
            response = self.getCdpId(self.node.credstick.address)  
        except (requests.exceptions.ConnectionError):
            self.add_frame(CupIDPromptFrame, height=22, width=70, title="CDP {} info".format(self.cup_id))
            return

        self.hide_wait_frame()

        # No registered cup id according to web api.
        # NOTE There *should* be a way to get cup ID onchain. 
        if len(response) == 0:
            self.add_frame(OpenCDPFrame, 20, 56, title="Open New CDP")
        else:
            self.cup_id = response[0]['id']
            lad = response[0]['lad']
            # If we directly own the CDP, need to migrate.
            if lad == self.node.credstick.address:
                self._migrate_cdp_at(lad)
                return

            self.ds_proxy = DsProxy(self.node, address=lad)
            self.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.cup_id))

            #ds_proxy_addr =  self.proxy_registry.proxies(self.recipient_addr_value())
            #if ds_proxy_addr is None:
                #    pass


    def _migrate_cdp_at(self, lad):
        # If a proxy exists, give.
        ds_proxy = self.dapp.proxy_registry.proxies(lad)
        if ds_proxy is not None:
            self.add_transaction_dialog(
                self.ds_proxy.give(
                    self.sai_proxy.address, 
                    self.tub.address, 
                    self.cup_id, 
                    target
                ),
                title="Set your proxy as CDP owner",
                gas_limit=55000
            )
            self.add_message_dialog("Migration step 2: give ownership to your proxy")
        else:
            self.add_transaction_dialog(
                self.proxy_registry.build(),
                title="Create CDP proxy",
                gas_limit=55000
            )
            self.add_message_dialog("Migration step 1: create proxy contract to own the CDP")

        self.add_message_dialog("This is an old style CDP setup that must be updated to work with the new CDP portal.")



    def getCdpId(self, address):
        address = address
        url = "https://mkr.tools/api/v1/lad/{}".format(address)
        response = requests.get(url).json()
        return response

    # cached properties, to save unnecessary queries of our dear friend infura

    @cached_property
    def peth_price(self):
        per = Decimal(self.tub.per())
        return per / self.RAY

    @cached_property
    def collateral_eth_value(self):
        return self.peth_price * self.collateral_peth_value

    @cached_property
    def liquidation_ratio(self):
        mat = Decimal(self.tub.mat())
        return  mat / self.RAY 

    @cached_property
    def cdp_liquidation_price(self):
        return self.liquidation_price(Decimal(self.tub.tab(self.cup_id)), self.collateral_eth_value)

    @cached_property
    def collateral_peth_value(self):
        return Decimal(self.tub.ink(self.cup_id))

    # abstract collateral price
    @cached_property
    def tag(self):
        return Decimal(self.tub.tag()) / self.RAY

    @cached_property
    def liquidation_penalty(self):
        axe = self.tub.axe()
        penalty = ((axe / self.RAY) - 1) * 100
        return round(Decimal(penalty), 2)

    @cached_property
    def debt_value(self):
        return Decimal(self.tub.tab(self.cup_id))

    @cached_property
    def global_dai_available(self):
        return Decimal(self.tub.rum()) 

    @cached_property
    def target_price(self):
        return Decimal(self.vox.par())

    @cached_property
    def system_collateralization_ratio(self):
        totalWethLocked = Decimal(self.tub.pie())
        wethPrice = Decimal(self.pip.eth_price()) / 10 ** 18
        daiSupply = Decimal(self.dai.totalSupply())
        targetPrice = Decimal(self.vox.par()) / self.RAY
        totalCollateralValue = totalWethLocked / self.WAD * wethPrice
        systemDaiDebt = daiSupply * targetPrice
        scr = totalCollateralValue / systemDaiDebt
        return scr * 10 ** 18 * 100

    @cached_property
    def peth_available_to_withdraw(self):
        return self.collateral_peth_value / self.WAD - Decimal(150) / self.tag /  Decimal(100) * self.debt_value / self.WAD 

    @property
    def eth_available_to_withdraw(self):
        return self.peth_price * self.peth_available_to_withdraw

    @property
    def dai_available_to_generate(self):
        debt_to_reach_150 =  ( Decimal(1) / (Decimal(1.50) / ( self.collateral_peth_value * self.tag )  ) ) / self.WAD
        return debt_to_reach_150 - (self.debt_value / self.WAD)

    @cached_property
    def ether_price(self):
        return self.pip.eth_price() / self.WAD

    @cached_property
    def mkr_price(self):
        return self.pep.mkr_price()


    @cached_property
    def stability_fee(self):
        fee = self.tub.fee()
        seconds_per_year = 60 * 60 * 24 * 365
        compounded_fee = (pow(fee / self.RAY, seconds_per_year) - 1) * 100
        return round(Decimal(compounded_fee), 2)

    @cached_property
    def mkr_stability_fee(self):
        return self.stability_fee / self.pep.mkr_price()

    # fee for this particular cdp
    @cached_property
    def cdp_stability_fee(self):
        return self.tub.rap(self.cup_id)

    # Takes and returns non WAD human units for payback amount
    def proportional_stability_fee(self, payback_amount):
        return (Decimal(payback_amount) * self.WAD / self.debt_value) * self.cdp_stability_fee / self.WAD
    # Takes and returns non WAD human units for payback amount
    def mkr_proportional_stability_fee(self, payback_amount):
        #debug(); pdb.set_trace()
        return  self.proportional_stability_fee(payback_amount) /  (self.mkr_price / self.WAD)

    @property
    def cdp_collateralization_ratio(self):
        return self.collateralization_ratio(self.collateral_peth_value, self.debt_value)

    def collateralization_ratio(self, cdp_collateral_peth_value, debt_value):
        coll_ratio = cdp_collateral_peth_value * self.tag / debt_value * Decimal(100)
        return round(coll_ratio, 3)

    def liquidation_price(self, debt_value, collateral_eth_value):
        return debt_value * self.liquidation_ratio / collateral_eth_value

    # lock Eth estimate methods
    #def projected_liquidation_price(self, cup_id, eth_to_deposit):
    #    projected_eth_collateral = self.collateral_eth_value(cup_id) + eth_to_deposit * self.WAD
    #    return self.liquidation_price(self.debt_value(cup_id), projected_eth_collateral)

    #def projected_collateralization_ratio(self, cup_id, eth_to_deposit):
    #    projected_peth_value = self.collateral_peth_value(cup_id) + eth_to_deposit * self.WAD / self.peth_price()
    #    return self.collateralization_ratio(projected_peth_value, self.debt_value(cup_id))

    def projected_collateralization_ratio(self, debt_value_change, eth_collateral_change):
        #projected_peth_value = self.collateral_peth_value(cup_id) + eth_to_deposit * self.WAD / self.peth_price()
        return self.collateralization_ratio(self.collateral_peth_value + (eth_collateral_change * self.WAD / self.peth_price), self.debt_value + debt_value_change)

    def projected_liquidation_price(self, debt_value_change, eth_collateral_change):
        #projected_eth_collateral = self.collateral_eth_value(cup_id) + eth_to_deposit * self.WAD
        return self.liquidation_price(self.debt_value + debt_value_change, self.collateral_eth_value + eth_collateral_change * self.WAD)




    # lock Eth methods

    def lock_peth(self, cdp_id, amount):
        #self.require_allowance('PETH', self.tub._contract.address, amount)
        self.add_transaction_dialog(self.tub.lock(cdp_id, amount), gas_limit=100000)
        #self.tub.lock(cdp_id, amount)

    def lock_weth(self, cdp_id, amount):
        #self.converter.weth2peth(amount)
        return self.lock_peth(cdp_id, amount)

    def lock_eth(self, cdp_id, amount):
        #self.converter.eth2weth(amount)
        self.lock_weth(cdp_id, amount)

    def lock(self):
        debug(); pdb.set_trace()
        self.lock_eth(self.cup_id, 0.05)



    def report(self):
        print("liquidation price: $", round(self.cdp_liquidation_price(cup_id), 3))
        print("ether price: $", self.ether_price())
        print("liquidation penalty: ", self.liquidation_penalty(), "%")
        print("collateralization ratio: ", self.cdp_collateralization_ratio(cup_id), "%")
        print("collateral peth value: PETH", round(self.node.w3.fromWei(self.collateral_peth_value(cup_id) , 'ether'), 3))
        print("collateral eth value: ETH", round(self.node.w3.fromWei(self.collateral_eth_value(cup_id), 'ether'), 3))
        print("yearly stability fee: ", self.stability_fee(), "%")
        print("CDP eth value: $", round( Decimal(self.pip.eth_price() / self.WAD) * self.node.w3.fromWei(self.collateral_eth_value(cup_id), 'ether'), 3) )
        print("global dai available: DAI ", round(self.global_dai_available() / self.WAD) )
        print("max available to withdraw PETH ", round(self.peth_available_to_withdraw(cup_id), 3) )
        print("max available to withdraw ETH ", round(self.eth_available_to_withdraw(cup_id), 3) )
        print("max available to withdraw value $", round(self.eth_available_to_withdraw(cup_id) * Decimal(self.pip.eth_price()) / self.WAD, 2))
        print("dai generated by cdp: DAI ", round(self.tub.tab(cup_id) / self.WAD, 2))
        print("max dai available to generate: DAI ", round(self.dai_available_to_generate(cup_id), 3))
        print("global CDP collateralization ratio: ", round(self.system_collateralization_ratio(), 4) )
        print("MKR price:  USD ", round(self.pep.mkr_price() / self.WAD, 3))
        debug(); pdb.set_trace()



