from shadowlands.sl_dapp import SLFrame

import decimal
from decimal import Decimal, InvalidOperation

import pdb
from shadowlands.tui.debug import debug

class FreeEthFrame(SLFrame):

    def proj_collat_ratio(self):
        try:
            return self.projected_collateralization_ratio 
        except:
            return "Unavailable"

    def initialize(self):
        self.add_label("How much ETH would you like to free?", add_divider=False)
        self.deposit_textbox_value = self.add_textbox("ETH Value:", default_value='')
        self.add_label("Max ETH available to withdraw:", add_divider=False)
        self.add_label("{:f}".format(self.dapp.eth_available_to_withdraw)[0:20])
        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)
        self.add_button_row([
            ("Free ETH", self.free_eth_choice, 0),
            ("Back", self.close, 1)
        ])

    def free_eth_choice(self):
        if self.deposit_eth_value() <= Decimal(0):
            self.dapp.add_message_dialog("Invalid ETH amount")
            return

        proj_ratio = self.dapp.projected_collateralization_ratio(0,  -1 * self.deposit_eth_value()) 

        if (proj_ratio / 100) < self.dapp.liquidation_ratio:
            self.dapp.add_message_dialog("You can't free that much ETH")
            return



        
        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.free(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address,
                self.dapp.cup_id, 
                self.deposit_eth_value() 
            ),
            title="Free Collateral",
            gas_limit=375013,
        )

        self.close()
        return

        self.close()

    def projected_liquidation_price(self):
        try:
            liq_price = self.dapp.projected_liquidation_price(0, -1 * self.deposit_eth_value())
            if liq_price < Decimal(0):
                return "Undefined"
            return "{:f}".format(liq_price)[0:12] + " USD"
        except (decimal.InvalidOperation):
            return "Undefined"

    def projected_collateralization_ratio(self):
        try:
            proj_ratio = self.dapp.projected_collateralization_ratio(0,  -1 * self.deposit_eth_value()) 
            if proj_ratio < Decimal(0):
                return "Undefined"
            return "{:f}".format(proj_ratio)[0:12] + " %"
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            return "Undefined"

    def deposit_eth_value_string(self):
        return str(self.deposit_eth_value())

    def deposit_eth_value(self):
        try:
            return Decimal(self.deposit_textbox_value() )
        except (TypeError, InvalidOperation):
            return Decimal(0.0)
