from shadowlands.sl_dapp import SLFrame

import decimal
from decimal import Decimal, InvalidOperation

import pdb
from shadowlands.tui.debug import debug

class GenerateDaiFrame(SLFrame):

    def proj_collat_ratio(self):
        try:
            return self.projected_collateralization_ratio 
        except:
            return "Unavailable"

    def initialize(self):
        self.add_label("How much DAI would you like to generate?", add_divider=False)
        self.deposit_textbox_value = self.add_textbox("DAI Value:", default_value='')
        self.add_label("Current account balance (ETH):", add_divider=False)
        self.add_label(str(self.dapp.dai_available_to_generate)[0:12])
        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)
        self.add_button_row([
            ("Borrow DAI", self.generate_dai_choice, 1),
            ("Back", self.close, 2)
        ], layout=[1, 1, 1])

    def generate_dai_choice(self):
        if self.deposit_eth_value() == Decimal(0.0):
            self.dapp.add_message_dialog("0 is not a valid choice")
            return

        
        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.draw(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address,
                self.dapp.cup_id, 
                self.deposit_eth_value() 
            ),
            title="Generate DAI",
            gas_limit=266611,
        )

        self.close()
        return
 

        self.close()

    def projected_liquidation_price(self):
        try:
            if self.deposit_eth_value() <= 0:
                return "Undefined"
            liq_price = self.dapp.projected_liquidation_price(self.deposit_eth_value() * self.dapp.WAD, 0)
            if liq_price == 0:
                return "Undefined"
            else:
                return "{:f}".format(liq_price)[0:12]
        except (decimal.InvalidOperation):
            return "Undefined"

    def projected_collateralization_ratio(self):
        try:
            if self.deposit_eth_value() <= 0:
                return "Undefined"
            coll_ratio = self.dapp.projected_collateralization_ratio(self.deposit_eth_value() * self.dapp.WAD, 0) 
            return "{:f}".format(coll_ratio)[0:12]
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            return "Undefined"

    def deposit_eth_value_string(self):
        return str(self.deposit_eth_value())

    def deposit_eth_value(self):
        try:
            return Decimal(self.deposit_textbox_value() )
        except (TypeError, InvalidOperation):
            return Decimal(0.0)
