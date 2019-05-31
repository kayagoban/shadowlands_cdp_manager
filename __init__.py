from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

from shadowlands.credstick import DeriveCredstickAddressError
from decimal import Decimal
from shadowlands.sl_contract import ContractConfigError
from shadowlands.tui.debug import debug
import pdb
import requests
import threading
import json
import logging

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

    def initialize(self):
        if self.node.network_name not in ["MainNet", "Kovan"]:
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet and Kovan")
            return
       
        self.show_wait_frame("Querying Maker's GraphQL API for CDP ID...")

        self.cup_id = None
        self.ds_proxy = None
        self.ds_proxy_address = None

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

        #threading.Thread(target=self.open_cdp).start()
        self.open_cdp()


    def open_cdp(self):
        self.ds_proxy_address = self.proxy_registry.proxies(self.node.credstick.address)

        if self.ds_proxy_address is not None:
            self.ds_proxy = DsProxy(self.node, address=self.ds_proxy_address)
            try:
                self.cup_id = self.find_cdp(self.ds_proxy_address)
            except:
                self.hide_wait_frame()
                self.add_message_dialog("Could not contact GraphQL")
                return

            if self.cup_id is not None:
                self.hide_wait_frame()
                self.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.cup_id))
                return

        try:
            self.cup_id = self.find_cdp(self.node.credstick.address)
        except:
            self.hide_wait_frame()
            self.add_message_dialog("Could not contact GraphQL")
            return

        if self.cup_id is not None:
            self.hide_wait_frame()
            self.migrate_cdp(self.node.credstick.address)
            return

        self.hide_wait_frame()
        self.add_frame(OpenCDPFrame, 24, 56, title="Open New CDP")


    def migrate_cdp(self, lad):
        if self.ds_proxy_address is not None:
            self.add_transaction_dialog(
                self.tub.give(
                    self.cup_id, 
                    self.ds_proxy_address
                ),
                title="Set your proxy as CDP owner",
                gas_limit=505000
            )
            self.add_message_dialog("Step 2 of 2: give ownership to proxy")
        else:
            self.add_transaction_dialog(
                self.proxy_registry.build(),
                title="Create CDP proxy",
                gas_limit=805000
            )
            self.add_message_dialog("Step 1 of 2: create proxy to own CDP")

        self.add_message_dialog("Updating CDP to work with the new CDP portal.")


    def find_cdp(self, address):
        endpoint = "https://sai-mainnet.makerfoundation.com/v1"
        data = 'query { allCups( condition: { lad: "' + address + '"  } ) { nodes { id, block, lad } } }' 

        response = requests.post(url = endpoint,headers={'Content-Type': 'application/graphql'}, data = data) 
        gqldata = json.loads(response.text)

        if gqldata['data']['allCups']['nodes'] == []:
            return None
        else:
            logging.info("Found cdp for {}: {}".format(address, gqldata))
            return gqldata['data']['allCups']['nodes'][0]['id']


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
        if self.cup_id is None:
            return Decimal(0)
        else:
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
        if self.cup_id is None:
            return Decimal(0)
        else:
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

    # fee for this particular cdp
    @cached_property
    def cdp_stability_fee(self):
        return self.tub.rap(self.cup_id)

    @cached_property
    def mkr_cdp_stability_fee(self):
        return self.cdp_stability_fee / self.mkr_price

    # Takes and returns non WAD human units for payback amount
    def proportional_stability_fee(self, payback_amount):
        return (Decimal(payback_amount) * self.WAD / self.debt_value) * self.cdp_stability_fee / self.WAD

    @property
    def mkr_stability_fee(self):
        return self.stability_fee / self.mkr_price


    @property
    def cdp_collateralization_ratio(self):
        return self.collateralization_ratio(self.collateral_peth_value, self.debt_value)

    def collateralization_ratio(self, cdp_collateral_peth_value, debt_value):
        coll_ratio = cdp_collateral_peth_value * self.tag / debt_value * Decimal(100)
        return round(coll_ratio, 3)

    def liquidation_price(self, debt_value, collateral_eth_value):
        return debt_value * self.liquidation_ratio / collateral_eth_value

    def projected_collateralization_ratio(self, debt_value_change, eth_collateral_change):
        return self.collateralization_ratio(self.collateral_peth_value + (eth_collateral_change * self.WAD / self.peth_price), self.debt_value + debt_value_change)

    def projected_liquidation_price(self, debt_value_change, eth_collateral_change):
        return self.liquidation_price(self.debt_value + debt_value_change, self.collateral_eth_value + eth_collateral_change * self.WAD)


    # lock Eth methods

    def lock_peth(self, cdp_id, amount):
        self.add_transaction_dialog(self.tub.lock(cdp_id, amount), gas_limit=100000)

    def lock_weth(self, cdp_id, amount):
        return self.lock_peth(cdp_id, amount)

    def lock_eth(self, cdp_id, amount):
        self.lock_weth(cdp_id, amount)

    def lock(self):
        debug(); pdb.set_trace()
        self.lock_eth(self.cup_id, 0.05)

