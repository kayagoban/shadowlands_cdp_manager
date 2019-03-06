from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

#import random, string
#from datetime import datetime, timedelta

from decimal import Decimal
from shadowlands.contract import ContractConfigError
from shadowlands.tui.debug import debug
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests
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

class CDPStatusFrame(SLFrame):

    def drop(self):
        debug(); pdb.set_trace()

    def initialize(self):
        #self.add_divider()
        
        self.add_label_quad("Liq. Price:", str(round(self.dapp.liquidation_price(self.dapp.cup_id), 4)) + " USD",
                            "Collat. Ratio:", str(round(self.dapp.collateralization_ratio(self.dapp.cup_id), 4)) + " %", add_divider=False)
        self.add_label_quad("Current Price:", str(round(self.dapp.ether_price(), 4)) + " USD",
                            "Minimum Ratio:", str(round(self.dapp.liquidation_ratio(), 4) * 100) + " %", add_divider=False)
        self.add_label_quad("Liq. penalty:", str(round(self.dapp.liquidation_penalty(), 4)) + " %",
                            "Stability Fee:", str(round(self.dapp.stability_fee(), 4)) + " %", add_divider=False)

        self.add_divider(draw_line=True)

        self.add_label("ETH Collateral")
        self.add_label_quad("Deposited:", str(round(self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " ETH",
                            "Max available:", str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id), 3)) + " ETH", add_divider=False)

        self.add_label_quad("", str(round(self.dapp.collateral_peth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " PETH",
                       "", str(round(self.dapp.peth_available_to_withdraw(self.dapp.cup_id), 3)) + " PETH", add_divider=False)

        self.add_label_quad("", str(round( Decimal(self.dapp.pip.eth_price() / self.dapp.WAD) * self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " USD",
                            "", str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id) * Decimal(self.dapp.pip.eth_price()) / self.dapp.WAD, 4)) + " USD", add_divider=True)
        self.add_ok_cancel_buttons(self.close, self.close, "DEPOSIT", cancel_text="WITHDRAW", cancel_index=2)
        self.add_divider(draw_line=True)

        self.add_label("DAI Position")
        self.add_label_quad("Generated:", str(round(self.dapp.tub.tab(self.dapp.cup_id) / self.dapp.WAD, 2)) +  " DAI",
                            "Max available:", str(round(self.dapp.dai_available_to_generate(self.dapp.cup_id), 3)) + " DAI", add_divider=False)
        self.add_divider(draw_line=False)
        self.add_ok_cancel_buttons(self.close, self.close, "PAY BACK", cancel_text="GENERATE", cancel_index=2)
        self.add_divider(draw_line=False)
        self.add_divider(draw_line=False)

        self.add_button(self.drop, "Quit", layout_distribution=[1, 1, 1, 1], layout_index=3)


class Dapp(SLDapp):

    cup_id = 15341
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


        self.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.cup_id))

    def getCdpIds():
        query = "query ($lad: String) {\n      allCups(condition: { lad: $lad }) {\n        nodes {\n          id\n        }\n      }\n    }"
        variables = '{"lad":"0x0E3873CC74F363aA38C2D8F1a29F6D1480078D55"}'

        # q = '{"query":"query ($lad: String) {\n      allCups(condition: { lad: $lad }) {\n        nodes {\n          id\n        }\n      }\n    }","variables":{"lad": "0x0E3873CC74F363aA38C2D8F1a29F6D1480078D55"}}'
        gql_string = '''{
  allCups(
    condition: {lad: "0x0E3873CC74F363aA38C2D8F1a29F6D1480078D55"}
  ){ 
    totalCount
    nodes {
        id 
    } 
  }  
}'''
        gql_string2 = '{ allCups(){ totalCount } }'


        #0x0E3873CC74F363aA38C2D8F1a29F6D1480078D55

        #query_string = query_string.replace('%s', self.node.credstick.address)

        #gql_string = gql(query)
        url = 'http://sai-mainnet.makerfoundation.com/v1'

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json' }

        debug(); pdb.set_trace()

        #response = requests.post(url, headers=headers, data=gql_string)
        response = requests.post(url, headers=headers, json={"query": gql_string2})
        #response = requests.post(url, data=query)
        #response = requests.post(url, data=query)

        debug(); pdb.set_trace()

        client = Client(transport=RequestsHTTPTransport(url='http://sai-mainnet.makerfoundation.com/v1'))
 


        client.execute(query)
 

        # from dai.js - get all cd ids for address
        #const api = new QueryApi(this._web3Service().networkId());
        #return api.getCdpIdsForOwner(address);
        #`query ($lad: String) {
        #allCups(condition: { lad: $lad }) {
        #  nodes {
        #    id
        #  }
        #}
        # }`

        #cup = tub.cup(15252)

        #self.report()

       #debug(); pdb.set_trace()

        #self.price_poller.eth_price




    def peth_price(self):
        per = Decimal(self.tub.per())
        return per / self.RAY
 
    def collateral_eth_value(self, cup_id):
        return self.peth_price() * self.collateral_peth_value(cup_id)

    def liquidation_ratio(self):
        mat = Decimal(self.tub.mat())
        return  mat / self.RAY 
        
    def liquidation_price(self, cup_id):
        debt_value = Decimal(self.tub.tab(cup_id)) # not quite, but..
        return debt_value * self.liquidation_ratio() / self.collateral_eth_value(cup_id)

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

    def collateralization_ratio(self, cup_id):
        tag = Decimal(self.tub.tag())
        coll_ratio = self.collateral_peth_value(cup_id) * (tag / self.RAY) / self.debt_value(cup_id) * Decimal(100)
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
        tag = Decimal(self.tub.tag())
        return self.collateral_peth_value(cup_id) / self.WAD - Decimal(150) / (tag/self.RAY) /  Decimal(100) * self.debt_value(cup_id) / self.WAD 

    def eth_available_to_withdraw(self, cup_id):
        return self.peth_price() * self.peth_available_to_withdraw(cup_id)

    def dai_available_to_generate(self, cup_id):
        tag = Decimal(self.tub.tag())
        debt_to_reach_150 =  ( Decimal(1) / (Decimal(1.50) / ( self.collateral_peth_value(cup_id) * (tag / self.RAY) )  ) ) / self.WAD
        return debt_to_reach_150 - (self.debt_value(cup_id) / self.WAD)

    def stability_fee(self):
        fee = self.tub.fee()
        seconds_per_year = 60 * 60 * 24 * 365
        compounded_fee = (pow(fee / self.RAY, seconds_per_year) - 1) * 100
        return round(Decimal(compounded_fee), 2)

    def ether_price(self):
        return self.pip.eth_price() / self.WAD

    def report(self):
        print("liquidation price: $", round(self.liquidation_price(cup_id), 3))
        print("ether price: $", self.ether_price())
        print("liquidation penalty: ", self.liquidation_penalty(), "%")
        print("collateralization ratio: ", self.collateralization_ratio(cup_id), "%")
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



