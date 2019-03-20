from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

#import random, string
#from datetime import datetime, timedelta

from shadowlands.credstick import DeriveCredstickAddressError
from decimal import Decimal
from shadowlands.contract import ContractConfigError
from shadowlands.tui.debug import debug
import requests
import threading
import pdb

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
from cdp_manager.contracts.peth import Peth

from cdp_manager.cdp_status_frame import CDPStatusFrame


class Dapp(SLDapp):

    RAY = Decimal(10 ** 27)
    WAD = Decimal(10 ** 18)

    #debug(); pdb.set_trace()

    def initialize(self):
        if self.node.network_name not in ["MainNet", "Kovan"]:
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet and Kovan")
            return
        
        self.tub = SaiTub(self.node)
        self.vox = SaiVox(self.node)
        self.dai = Dai(self.node)
        self.pip = SaiPip(self.node)
        self.pep = SaiPep(self.node)
        self.peth = Peth(self.node) 

        self.erc2_contract = { 'DAI': self.dai, 'PETH': self.peth }

        #debug(); pdb.set_trace()
        self.show_wait_frame()

        threading.Thread(target=self._cdp_id_worker).start()


    def _cdp_id_worker(self):
        try:

            response = self.getCdpId(self.node.credstick.address)  
            self.cup_id = response[0]['id']
            self.lad = response[0]['lad']

            self.hide_wait_frame()
            self.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.cup_id))
        except IndexError:
            debug(); pdb.set_trace()
        except DeriveCredstickAddressError:
            self.hide_wait_frame()
            self.add_message_dialog("Error occured obtaining the CDP ID")


    def getCdpId(self, address):
        address = address
        url = "https://mkr.tools/api/v1/lad/{}".format(address)
        response = requests.get(url).json()
        return response
        #debug(); pdb.set_trace()

    def peth_price(self):
        per = Decimal(self.tub.per())
        return per / self.RAY
 
    def collateral_eth_value(self, cup_id):
        return self.peth_price() * self.collateral_peth_value(cup_id)

    def liquidation_ratio(self):
        mat = Decimal(self.tub.mat())
        return  mat / self.RAY 
        
    def cdp_liquidation_price(self, cup_id):
        return self.liquidation_price(Decimal(self.tub.tab(cup_id)), self.collateral_eth_value(cup_id))

    def liquidation_price(self, debt_value, collateral_eth_value):
        return debt_value * self.liquidation_ratio() / collateral_eth_value

    def collateral_peth_value(self, cup_id):
        return Decimal(self.tub.ink(cup_id))

    # abstract collateral price
    def tag(self):
        return Decimal(self.tub.tag()) / self.RAY

    def liquidation_penalty(self):
        axe = self.tub.axe()
        penalty = ((axe / self.RAY) - 1) * 100
        return round(Decimal(penalty), 2)

    def debt_value(self, cup_id):
        return Decimal(self.tub.tab(cup_id))

    def global_dai_available(self):
        return Decimal(self.tub.rum()) 

    def target_price(self):
        return Decimal(self.vox.par())

    def cdp_collateralization_ratio(self, cup_id):
        return self.collateralization_ratio(self.collateral_peth_value(cup_id), self.debt_value(cup_id))

    def collateralization_ratio(self, cdp_collateral_peth_value, debt_value):
        coll_ratio = cdp_collateral_peth_value * self.tag() / debt_value * Decimal(100)
        return round(coll_ratio, 3)

    def system_collateralization_ratio(self):
        totalWethLocked = Decimal(self.tub.pie())
        wethPrice = Decimal(self.pip.eth_price()) / 10 ** 18
        daiSupply = Decimal(self.dai.totalSupply())
        targetPrice = Decimal(self.vox.par()) / self.RAY
        totalCollateralValue = totalWethLocked / self.WAD * wethPrice
        systemDaiDebt = daiSupply * targetPrice
        scr = totalCollateralValue / systemDaiDebt
        return scr * 10 ** 18 * 100

    def peth_available_to_withdraw(self, cup_id):
        return self.collateral_peth_value(cup_id) / self.WAD - Decimal(150) / self.tag() /  Decimal(100) * self.debt_value(cup_id) / self.WAD 

    def eth_available_to_withdraw(self, cup_id):
        return self.peth_price() * self.peth_available_to_withdraw(cup_id)

    def dai_available_to_generate(self, cup_id):
        debt_to_reach_150 =  ( Decimal(1) / (Decimal(1.50) / ( self.collateral_peth_value(cup_id) * self.tag() )  ) ) / self.WAD
        return debt_to_reach_150 - (self.debt_value(cup_id) / self.WAD)

    def stability_fee(self):
        fee = self.tub.fee()
        seconds_per_year = 60 * 60 * 24 * 365
        compounded_fee = (pow(fee / self.RAY, seconds_per_year) - 1) * 100
        return round(Decimal(compounded_fee), 2)

    def ether_price(self):
        return self.pip.eth_price() / self.WAD



    # lock Eth estimate methods
    def projected_liquidation_price(self, cup_id, eth_to_deposit):
        projected_eth_collateral = self.collateral_eth_value(cup_id) + eth_to_deposit * self.WAD
        return self.liquidation_price(self.debt_value(cup_id), projected_eth_collateral)

    def projected_collateralization_ratio(self, cup_id, eth_to_deposit):
        projected_peth_value = self.collateral_peth_value(cup_id) + eth_to_deposit * self.WAD / self.peth_price()
        return self.collateralization_ratio(projected_peth_value, self.debt_value(cup_id))



    # lock Eth methods

    def lock_peth(self, cpd_id, amount):
        self.require_allowance('PETH', self.tub._contract.address, amount)
        self.tub.lock(cdp_id, amount)

    def lock_weth(self, cdp_id, amount):
        #self.converter.weth2peth(amount)
        return self.lock_peth(cdp_id, amount)

    def lock_eth(self, cdp_id, amount):
        #self.converter.eth2weth(amount)
        self.lock_weth(cdp_id, amount)

    def lock(self):
        debug(); pdb.set_trace()
        self.lock_eth(self.cup_id, 0.05)


    '''
    async requireAllowance(
    tokenSymbol,
    receiverAddress,
    { estimate = maxAllowance, promise }
  ) {
    const token = this.get('token').getToken(tokenSymbol);
    const ownerAddress = this.get('token')
      .get('web3')
      .currentAddress();
    const allowance = await token.allowance(ownerAddress, receiverAddress);

    if (allowance.lt(maxAllowance.div(2)) && !this._shouldMinimizeAllowance) {
      const tx = await token.approveUnlimited(receiverAddress, { promise });
      this.get('event').emit('allowance/APPROVE', {
        transaction: tx
      });
      return tx;
    }

    if (allowance.lt(estimate) && this._shouldMinimizeAllowance) {
      const tx = await token.approve(receiverAddress, estimate, { promise });
      this.get('event').emit('allowance/APPROVE', {
        transaction: tx
      });
    }
    }
    
    @tracksTransactions
      async lockPeth(cdpId, amount, { unit = PETH, promise }) {
        const hexCdpId = numberToBytes32(cdpId);
        const value = getCurrency(amount, unit).toEthersBigNumber('wei');
        await this.get('allowance').requireAllowance(
          PETH,
          this._tubContract().address,
          { promise }
        );
        return this._tubContract().lock(hexCdpId, value, {
          promise
        });
      }

      async lockWeth(cdpId, amount, { unit = WETH, promise }) {
        const wethPerPeth = await this.get('price').getWethToPethRatio();
        const weth = getCurrency(amount, unit);
        await this._conversionService().convertWethToPeth(weth, {
          promise
        });

        return this.lockPeth(cdpId, weth.div(wethPerPeth), { promise });
      }

      async lockEth(cdpId, amount, { unit = ETH, promise }) {
        const convert = this._conversionService().convertEthToWeth(amount, {
          unit,
          promise
        });
        await this._txMgr().confirm(convert);
        return this.lockWeth(cdpId, amount, { promise });
      }

      
    '''


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



