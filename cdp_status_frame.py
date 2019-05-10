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
# from concurrent.futures._base import TimeoutError


import pdb


class CDPStatusFrame(SLFrame):

    def lock_eth_frame(self):
        self.dapp.add_frame(LockEthFrame, 15, 50, title="Deposit Collateral")
        self.close()

    def free_eth_frame(self):
        self.dapp.add_frame(FreeEthFrame, 15, 50, title="Free Collateral")
        self.close()

    def payback_dai_frame(self):
        self.dapp.add_frame(PaybackDaiFrame, 21, 50, title="Pay back DAI")
        self.close()

    def generate_dai_frame(self):
        self.dapp.add_frame(GenerateDaiFrame, 15, 50, title="Borrow DAI")
        self.close()

    def close_cdp_frame(self):
        self.dapp.add_frame(CloseCDPFrame, 20, 50, title="Close CDP")
        self.close()

    def move_cdp_frame(self):
        self.dapp.add_frame(GiveCDPFrame, 20, 59, title="Transfer CDP to different address")
        self.close()

    def refresh_info(self):
        pass

    def initialize(self):
        #self.add_divider()
        
        try:
            try:
                liq_price = str(round(self.dapp.cdp_liquidation_price, 4)) + " USD"
            except (decimal.InvalidOperation):
                liq_price = "Undefined"

            try:
                collat_ratio = str(round(self.dapp.cdp_collateralization_ratio, 4)) + " %"
            except (decimal.InvalidOperation):
                collat_ratio = "Undefined"

            try:
                max_avail = str(round(self.dapp.eth_available_to_withdraw, 3)) 
            except (decimal.InvalidOperation):
                max_avail = "Undefined"

            try:
                dai_max_avail = str(round(self.dapp.dai_available_to_generate, 3)) + " DAI"
            except (decimal.DivisionByZero):
                dai_max_avail = "Undefined" 


            self.add_label_quad("Liq. Price:", 
                                liq_price,
                                "Collat. Ratio:", 
                                collat_ratio, 
                                add_divider=False)

            self.add_label_quad("Current Price:", 
                                str(round(self.dapp.ether_price, 4)) + " USD", 
                                "Minimum Ratio:", 
                                str(round(self.dapp.liquidation_ratio, 4) * 100) + " %", add_divider=False)

            self.add_label_quad("Liq. penalty:", 
                                str(round(self.dapp.liquidation_penalty, 4)) + " %", 
                                "Stability Fee:", 
                                str(self.dapp.stability_fee)[0:6] + " %", 
                                add_divider=False)

            self.add_divider(draw_line=True)

            self.add_label("ETH Collateral")

            self.add_label_quad("Deposited:", 
                                str(round(self.dapp.collateral_eth_value / self.dapp.WAD, 4)) +  " ETH",
                                "Max available:", 
                                max_avail + " ETH", 
                                add_divider=False)

            self.add_label_quad("", str(round(self.dapp.collateral_peth_value / self.dapp.WAD, 4)) +  " PETH",
                                "", str(round(self.dapp.peth_available_to_withdraw, 3)) + " PETH", add_divider=False)
            self.add_label_quad("", str(round( self.dapp.ether_price * self.dapp.collateral_eth_value / self.dapp.WAD, 4)) +  " USD",
                                "", str(round(self.dapp.eth_available_to_withdraw * self.dapp.ether_price, 4)) + " USD", add_divider=False)
            self.add_button_row(
                [
                    ("Deposit ", self.lock_eth_frame, 0),
                    ("Withdraw", self.free_eth_frame, 2)
                ],
                layout=[1, 1, 1, 1]
            )
     
            self.add_divider()
            
            self.add_divider(draw_line=True)

            self.add_label("DAI Position")
            self.add_label_quad("Generated:", str(round(self.dapp.debt_value / self.dapp.WAD, 2)) +  " DAI",
                                "Max available:", dai_max_avail, add_divider=False)
            self.add_divider(draw_line=False)
            self.add_button_row(
                [
                    ("Pay back", self.payback_dai_frame, 0),
                    ("Generate", self.generate_dai_frame, 2)
                ],
                layout=[1, 1, 1, 1]
            )
            self.add_divider()
            self.add_divider(draw_line=True)
            #self.add_divider()
            self.add_button_row(
                [
                    ("Move CDP", self.move_cdp_frame, 0),
                    ("Close CDP", self.close_cdp_frame, 1),
                    ("Back", self.close, 3) 
                ],
                [1, 1, 1, 1]
            )

        except TimeoutError:
            self.dapp.add_message_dialog("Timed out trying to get CDP status")
            self.close()

            



