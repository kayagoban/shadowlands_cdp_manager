from shadowlands.sl_dapp import SLFrame
import decimal
from decimal import Decimal
#from decimal import DivisionUndefined

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
from cdp_manager.payback_dai_frame import PaybackDaiFrame
from cdp_manager.generate_dai_frame import GenerateDaiFrame
from cdp_manager.free_eth_frame import FreeEthFrame
from cdp_manager.close_cdp_frame import CloseCDPFrame
from cdp_manager.give_cdp_frame import GiveCDPFrame


import pdb


class CDPStatusFrame(SLFrame):

    def drop(self):
        debug(); pdb.set_trace()

    def payback_dai_frame(self):
        self.dapp.add_frame(PaybackDaiFrame, 20, 50, title="Free Collateral")

    def generate_dai_frame(self):
        self.dapp.add_frame(GenerateDaiFrame, 20, 50, title="Free Collateral")

    def free_eth_frame(self):
        self.dapp.add_frame(FreeEthFrame, 20, 50, title="Free Collateral")


    def lock_eth_frame(self):
        #require_allowance(self, symbol, receiver_address, amount):
        #erc_contract.approve(receiver_address, amount * self.WAD)
        #debug(); pdb.set_trace()
        #self.dapp.lad


        # approve unlimited.. ?
        #if self.dapp.peth.allowance(self.dapp.peth.address, self.dapp.tub.address) < Decimal(2 ** 128 - 1):
        #    erc_contract.approveUnlimited(receiver_address)


        self.dapp.add_frame(LockEthFrame, 20, 50, title="Deposit Collateral")

    def close_cdp_frame(self):
        self.dapp.add_frame(CloseCDPFrame, 20, 50, title="Close CDP")
        self.close()

    def move_cdp_frame(self):
        self.dapp.add_frame(GiveCDPFrame, 20, 59, title="Transfer CDP to different address")

    def refresh_info(self):
        pass

    def initialize(self):
        #self.add_divider()
        
        try:
            liq_price = str(round(self.dapp.cdp_liquidation_price(self.dapp.cup_id), 4)) + " USD"
        except (decimal.InvalidOperation):
            liq_price = "Undefined"

        try:
            collat_ratio = str(round(self.dapp.cdp_collateralization_ratio(self.dapp.cup_id), 4)) + " %"
        except (decimal.InvalidOperation):
            collat_ratio = "Undefined"

        try:
            max_avail = str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id), 3)) 
        except (decimal.InvalidOperation):
            max_avail = "Undefined"

        try:
            dai_max_avail = str(round(self.dapp.dai_available_to_generate(self.dapp.cup_id), 3)) + " DAI"
        except (decimal.DivisionByZero):
            dai_max_avail = "Undefined" 


        
        self.add_ok_cancel_buttons(self.move_cdp_frame, cancel_fn=self.close_cdp_frame, ok_text="Move CDP", cancel_text="Close CDP", ok_index=2, cancel_index=3)

        self.add_divider(draw_line=True)

        self.add_label_quad("Liq. Price:", 
                            liq_price,
                            "Collat. Ratio:", 
                            collat_ratio, 
                            add_divider=False)

        self.add_label_quad("Current Price:", 
                            str(round(self.dapp.ether_price(), 4)) + " USD", 
                            "Minimum Ratio:", 
                            str(round(self.dapp.liquidation_ratio(), 4) * 100) + " %", add_divider=False)

        self.add_label_quad("Liq. penalty:", 
                            str(round(self.dapp.liquidation_penalty(), 4)) + " %", 
                            "Stability Fee:", 
                            str(round(self.dapp.stability_fee(), 4)) + " %", 
                            add_divider=False)

        self.add_divider(draw_line=True)

        self.add_label("ETH Collateral")

        self.add_label_quad("Deposited:", 
                            str(round(self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " ETH",
                            "Max available:", 
                            max_avail + " ETH", 
                            add_divider=False)

        self.add_label_quad("", str(round(self.dapp.collateral_peth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " PETH",
                            "", str(round(self.dapp.peth_available_to_withdraw(self.dapp.cup_id), 3)) + " PETH", add_divider=False)
        self.add_label_quad("", str(round( Decimal(self.dapp.pip.eth_price() / self.dapp.WAD) * self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " USD",
                            "", str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id) * Decimal(self.dapp.pip.eth_price()) / self.dapp.WAD, 4)) + " USD", add_divider=False)
        self.add_ok_cancel_buttons(self.lock_eth_frame, self.free_eth_frame, "DEPOSIT", cancel_text="WITHDRAW", cancel_index=2)
        
        self.add_divider(draw_line=True)

        self.add_label("DAI Position")
        self.add_label_quad("Generated:", str(round(self.dapp.tub.tab(self.dapp.cup_id) / self.dapp.WAD, 2)) +  " DAI",
                            "Max available:", dai_max_avail, add_divider=False)
        self.add_divider(draw_line=False)
        self.add_ok_cancel_buttons(self.payback_dai_frame, self.generate_dai_frame, "PAY BACK", cancel_text="GENERATE", cancel_index=2)
        self.add_divider(draw_line=True)
        #self.add_divider(draw_line=False)

        self.add_ok_cancel_buttons(self.refresh_info, ok_text="Refresh", cancel_text="Quit", ok_index=2, cancel_index=3)


