from shadowlands.sl_dapp import SLFrame
import decimal
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
from cdp_manager.payback_dai_frame import PaybackDaiFrame
from cdp_manager.generate_dai_frame import GenerateDaiFrame
from cdp_manager.free_eth_frame import FreeEthFrame
from cdp_manager.close_cdp_frame import CloseCDPFrame
from cdp_manager.give_cdp_frame import GiveCDPFrame

import pdb

class CDPStatusFrame(SLFrame):

    def lock_eth_frame(self):
        self.dapp.add_frame(LockEthFrame, 15, 50, title="Deposit Collateral")

    def free_eth_frame(self):
        self.dapp.add_frame(FreeEthFrame, 15, 50, title="Free Collateral")

    def payback_dai_frame(self):
        self.dapp.add_frame(PaybackDaiFrame, 18, 50, title="Pay back DAI")

    def generate_dai_frame(self):
        self.dapp.add_frame(GenerateDaiFrame, 15, 50, title="Borrow DAI")

    def close_cdp_frame(self):
        self.dapp.add_frame(CloseCDPFrame, 13, 50, title="Close CDP")
        self.close()

    def move_cdp_frame(self):
        self.dapp.add_frame(GiveCDPFrame, 6, 59, title="Transfer CDP to different address")
        self.close()

    def refresh_info(self):
        cproperties = [
            'peth_price',
            'collateral_eth_value',
            'liquidation_ratio',
            'cdp_liquidation_price',
            'collateral_peth_value',
            'tag',
            'liquidation_penalty',
            'debt_value',
            'global_dai_available',
            'target_price',
            'system_collateralization_ratio',
            'peth_available_to_withdraw',
            'eth_available_to_withdraw',
            'dai_available_to_generate',
            'ether_price',
            'mkr_price',
            'stability_fee',
            'cdp_stability_fee',
            'mkr_cdp_stability_fee'
        ]

        for cproperty in cproperties:
            try:
                del self.dapp.__dict__[cproperty]
            except KeyError:
                # If property not yet cached, this will happen.
                pass

        self.dapp.add_message_dialog("Refreshing stats.")


    

    def initialize(self):
        try:

            self.add_label_quad("Liq. Price:", 
                                lambda: self.show_divisible('cdp_liquidation_price', 'USD'),
                                "Collat. Ratio:", 
                                lambda: self.show_divisible('cdp_collateralization_ratio', '%'), 
                                add_divider=False)

            self.add_label_quad("Current Price:", 
                                lambda: self.show_number(self.dapp.ether_price, 'USD'), 
                                "Minimum Ratio:", 
                                lambda: self.show_number(self.dapp.liquidation_ratio * 100, "%"), add_divider=False)

            self.add_label_quad("Liq. penalty:", 
                                lambda: self.show_number(self.dapp.liquidation_penalty, "%"), 
                                "Stability Fee:", 
                                lambda: self.show_number(self.dapp.stability_fee, "%"), 
                                add_divider=False)

            self.add_divider(draw_line=True)

            self.add_label("ETH Collateral")

            self.add_label_quad("Deposited:", 
                                lambda: self.show_number(self.dapp.collateral_eth_value / self.dapp.WAD, "ETH"),
                                "Max available:", 
                                lambda: self.show_divisible('eth_available_to_withdraw', "ETH"), 
                                add_divider=False)

            self.add_label_quad("", lambda: self.show_number(self.dapp.collateral_peth_value / self.dapp.WAD,"PETH"),
                                "", lambda: self.show_number(self.dapp.peth_available_to_withdraw,"PETH"), add_divider=False)
            self.add_label_quad("", lambda: self.show_number(self.dapp.ether_price * self.dapp.collateral_eth_value / self.dapp.WAD,"USD"),
                                "", lambda: self.show_number(self.dapp.eth_available_to_withdraw * self.dapp.ether_price, "USD"), add_divider=False)
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
            self.add_label_quad("Generated:", lambda: self.show_number(self.dapp.debt_value / self.dapp.WAD, 'DAI'),
                                "Max available:", lambda: self.show_divisible('dai_available_to_generate', 'DAI'), add_divider=False)
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
            self.add_button_row(
                [
                    ("Move CDP", self.move_cdp_frame, 0),
                    ("Close CDP", self.close_cdp_frame, 1),
                    ("Refresh", self.refresh_info, 2),
                    ("Back", self.close, 3) 
                ],
                [1, 1, 1, 1]
            )

        except TimeoutError:
            self.dapp.add_message_dialog("Timed out trying to get CDP status")
            self.close()

    def show_number(self, number, denomination=None):
        display_value = str(number)[:8]
        if denomination is not None:
            display_value += " {}".format(denomination)
        return display_value
            
    def p_fn(self, p_str):
        '''
        I got myself into a pickle trying to create a decorator
        for cached properties.  This lets us execute the underlying
        function when we feel like it.
        '''
        from cdp_manager.__init__ import Dapp
        p_obj = Dapp.__dict__[p_str]
        return p_obj.__get__(self.dapp, Dapp)


    def show_divisible(self, fn, denomination=None):

        try:
            if fn.__class__ == str:
                number = self.p_fn(fn)
            else:
                number = fn()

            if number == 0:
                return "Undefined"
            divisible = str(number)[:8]
            if denomination is not None:
                divisible += " {}".format(denomination)
            return divisible
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            divisible = "Undefined" 
        return divisible





