from shadowlands.sl_dapp import SLFrame

import decimal
from decimal import Decimal, InvalidOperation

import pdb
from shadowlands.tui.debug import debug

class PaybackDaiFrame(SLFrame):

    def proj_collat_ratio(self):
        try:
            return self.projected_collateralization_ratio 
        except:
            return "Unavailable"

    def initialize(self):

        self.add_divider()
        self.add_label("Current account balance (ETH):", add_divider=False)
        self.add_label(str(round(self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)), add_divider=False)
        self.add_divider(draw_line=True)
        self.add_label("How much DAI would you like to pay back?", add_divider=False)
        self.deposit_textbox_value = self.add_textbox("DAI Value:", default_value='1')
        self.add_divider(draw_line=True)
        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)
        self.add_ok_cancel_buttons(self.wipe_dai_choice, ok_text="Free ETH")

    def wipe_dai_choice(self):
        if self.deposit_eth_value() == Decimal(0.0):
            self.dapp.add_message_dialog("0 ETH is not a valid choice")
            return

        # check to see if DAI spending is unlocked for contract
        #debug(); pdb.set_trace()
        allowance = self.dapp.mkr.allowance(
            self.dapp.node.credstick.address, 
            self.dapp.ds_proxy.address
        )

        if allowance == 0:
            self.dapp.add_transaction_dialog(
                self.dapp.mkr.approve(
                    self.dapp.ds_proxy.address, 
                    self.dapp.MAX_WEI
                ),
                title="Allow cdp proxy to send MKR",
                gas_limit=50000,
            )
            self.dapp.add_message_dialog("First we must allow the CDP proxy to send MKR")
        else:
            self.dapp.add_transaction_dialog(
                self.dapp.ds_proxy.wipe(
                    self.dapp.sai_proxy.address, 
                    self.dapp.tub.address,
                    self.dapp.cup_id, 
                    self.deposit_eth_value() 
                ),
                title="Pay back MKR",
                gas_limit=375013,
            )

        self.close()
        return
 

    def projected_liquidation_price(self):
        try:
            return str(round(self.dapp.projected_liquidation_price(self.dapp.cup_id, -(self.deposit_eth_value()), 0), 4))
        except (decimal.InvalidOperation):
            return "Undefined"

    def projected_collateralization_ratio(self):
        try:
            return str(round(self.dapp.projected_collateralization_ratio(self.dapp.cup_id, -(self.deposit_eth_value()), 0), 4))
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            return "Undefined"

    def deposit_eth_value_string(self):
        return str(self.deposit_eth_value())

    def deposit_eth_value(self):
        try:
            return Decimal(self.deposit_textbox_value() )
        except (TypeError, InvalidOperation):
            return Decimal(0.0)
