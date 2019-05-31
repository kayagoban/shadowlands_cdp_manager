from shadowlands.sl_dapp import SLFrame

import decimal
from decimal import Decimal, InvalidOperation

import pdb
from shadowlands.tui.debug import debug

class LockEthFrame(SLFrame):

    def proj_collat_ratio(self):
        try:
            return self.projected_collateralization_ratio 
        except:
            return "Unavailable"

    def initialize(self):
        self.add_label("How much ETH would you like to deposit?", add_divider=False)
        self.deposit_textbox_value = self.add_textbox("ETH Value:", default_value='1')
        self.add_label("Current account balance (ETH):", add_divider=False)
        self.add_label("{:f}".format(self.dapp.node.eth_balance)[0:12])
        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)
        self.add_button_row(
            [
                ("Deposit", self.lock_eth_choice, 0),
                ("Back", self.close, 1)
            ]
        )

    def lock_eth_choice(self):
        if self.deposit_eth_value() < Decimal(0):
            self.dapp.add_message_dialog("Not a valid deposit amount")
            return
            

        #debug(); pdb.set_trace()

        
        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.lock(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address,
                self.dapp.cup_id, 
            ),
            tx_value=self.deposit_eth_value(),
            title="Lock Collateral",
            gas_limit=300000,
        )

        self.close()
        return
 

        self.close()

    def projected_liquidation_price(self):
        try:
            liq_price = self.dapp.projected_liquidation_price(0, self.deposit_eth_value())
            if liq_price < Decimal(0):
                return "Undefined"
            return "{:f}".format(liq_price)[0:12] + " USD"
        except (decimal.InvalidOperation):
            return "Undefined"

    def projected_collateralization_ratio(self):
        try:
            proj_ratio = self.dapp.projected_collateralization_ratio(0,  self.deposit_eth_value())
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
