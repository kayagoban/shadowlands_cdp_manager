from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

#import random, string
#from datetime import datetime, timedelta

from shadowlands.contract import ContractConfigError
from shadowlands.tui.debug import debug
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

from decimal import Decimal

class Dapp(SLDapp):

    RAY = 10 ** 27

    def collateral_peth_value(self, cup_id):
        return self.tub.ink(cup_id)
 
    def collateral_eth_value(self, cup_id):
        per = self.tub.per()
        peth_price = per / self.RAY
        return peth_price * self.collateral_peth_value(cup_id)
        
    def liquidation_price(self, cup_id):
        debt_value = self.tub.tab(cup_id) # not quite, but..
        mat = self.tub.mat()
        liquidation_ratio = mat / self.RAY 
        return round(Decimal( debt_value * liquidation_ratio / self.collateral_eth_value(cup_id)), 2)

    def liquidation_penalty(self):
        axe = self.tub.axe()
        penalty = ((axe / self.RAY) - 1) * 100
        return round(Decimal(penalty), 2)

    def debt_value(self, cup_id):
        return self.tub.tab(cup_id)

    def collateralization_ratio(self, cup_id):
        self.debt_value(cup_id)

        tag = self.tub.tag()

        target_price = self.vox.par()
        usd_debt = tag * target_price
        
        per = self.tub.per()
        peth_price = per / self.RAY

        coll_ratio = self.collateral_peth_value(15252) * (self.tub.tag() / self.RAY) / self.debt_value(cup_id) * 100
        return round(Decimal(coll_ratio), 2)

# async getCollateralizationRatio(cdpId) {
#    const usdDebt = await this.getDebtValue(cdpId, USD);
#    // avoid division by 0
#    if (usdDebt.eq(0)) return Infinity;
#
#    const [pethPrice, pethCollateral] = await Promise.all([
#      this.get('price').getPethPrice(),
#      this.getCollateralValue(cdpId, PETH)
#    ]);
#    return pethCollateral
#      .times(pethPrice)
#      .div(usdDebt)
#      .toNumber();
#  }


    def report(self):
        cup_id = 15252
        print("liquidation price: $", self.liquidation_price(cup_id))
        print("ether price: $", self.price_poller.eth_price)
        print("liquidation penalty: ", self.liquidation_penalty(), "%")
        print("collateralization ratio: ", self.collateralization_ratio(cup_id), "%")

    def initialize(self):
        #self.name = None  # The full name given by the user
        #self.subdomain = None  # just the subdomain
        #self.domain = None # just the domain.eth
        #self.resolved_address = None 

        if self.node.network_name not in ["MainNet", "Kovan"]:
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet and Kovan")
            return
        
        self.tub = SaiTub(self.node)
        self.vox = SaiVox(self.node)

        #cup = tub.cup(15252)

        #self.report()

        debug(); pdb.set_trace()

        #debug(); pdb.set_trace()

        #self.price_poller.eth_price

        self.add_frame(CDPStatusFrame, height=20, width=55, title="CDP info")
  # this.getDebtValue(cdpId, USD),
        #debt_value = 

     # this.getLiquidationRatio(),
     # this.getCollateralValue(cdpId)

     #   liquidation_price = debt_value * liquidation_ratio / collateral_value

'''  
async getLiquidationPenalty() {
    const value = await this._tubContract().axe();

    return new BigNumber(value.toString())
      .dividedBy(RAY)
      .minus(1)
      .toNumber();
  }

'''
      

        #try:
            #    pass
            #except (ContractConfigError):
                #    self.add_message_dialog("Could not load the contracts for this Dapp.")
                #    return None



