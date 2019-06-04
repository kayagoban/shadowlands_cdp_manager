from shadowlands.sl_dapp import SLFrame

import decimal
from decimal import Decimal, InvalidOperation, DivisionByZero

import pdb
from shadowlands.tui.debug import debug

class PaybackDaiFrame(SLFrame):

    def proj_collat_ratio(self):
        try:
            return self.projected_collateralization_ratio 
        except:
            return "Unavailable"

    def initialize(self):

        self.add_label("How much DAI would you like to pay back?", add_divider=False)
        self.deposit_textbox_value = self.add_textbox("DAI Value:", default_value='')
        
        self.add_label("Outstanding DAI debt:", add_divider=False)
        self.add_label_with_button(
            "{:f}".format( self.debt_value())[0:16] + " DAI", "Get DAI", self.dai_uniswap_frame
        )

        self.add_label(self.stability_fee_label, add_divider=False)
        self.add_label_with_button(self.stability_fee, "Get MKR", self.mkr_uniswap_frame)
        #self.add_label(self.stability_fee)

        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)
        self.add_button_row(
            [
                ("Pay back DAI", self.wipe_dai_choice, 0),
                #("Get MKR", self.uniswap_frame, 1),
                ("Back", self.close, 2)
            ], 
            layout=[6, 5, 5]
        )

    def debt_value(self):
        try:
            debt = self.dapp.debt_value / self.dapp.WAD 
        except InvalidOperation:
            return Decimal(0)

        return debt
                                   

    def mkr_uniswap_frame(self):
        self.dapp.add_uniswap_frame(self.dapp.mkr.address, action='buy', buy_amount=self.uniswap_to_buy_mkr_value())
        self.close()

    def dai_uniswap_frame(self):
        self.dapp.add_uniswap_frame(self.dapp.dai.address, action='buy', buy_amount=self.debt_value())
        self.close()



    # This is a stand-in for an actual radio button, which would
    # allow a choice of DAI vs. MKR to pay the fee.  
    # Hardcoded to MKR for now.
    def uniswap_to_buy_mkr_value(self):
        if self.deposit_eth_value() == 0:
            return Decimal(0)
        sfee = self.dapp.proportional_stability_fee( self.deposit_eth_value())
        return sfee + sfee * Decimal(0.01)

    def stability_fee_label(self):
        return "Stability fee(MKR):"

    def stability_fee(self):
        try:
            fee = self.dapp.proportional_stability_fee(
                self.deposit_eth_value()
            ) 

            if fee <= Decimal('0'):
                return ""

            return "{:f}".format(fee)[0:16] + " MKR"
        except DivisionByZero:
            return ""


    def wipe_dai_choice(self):

        if self.deposit_eth_value() == Decimal(0.0):
            self.dapp.add_message_dialog("0 is not a valid choice")
            return

        # check to see if token spending is unlocked for contract
        fee_denomination = 'MKR'

        if fee_denomination == 'MKR':
            fee_erc20_contract = self.dapp.mkr
        elif fee_denomination == 'DAI':
            fee_erc20_contract = self.dapp.dai


        for erc in [('MKR', self.dapp.mkr), ('DAI', self.dapp.dai)]:
            allowance = erc[1].allowance(
                self.dapp.node.credstick.address, 
                self.dapp.ds_proxy.address
            )
            
            if allowance == 0:
                self.dapp.add_transaction_dialog(
                    erc[1].approve(
                        self.dapp.ds_proxy.address, 
                        self.dapp.MAX_WEI
                    ),
                    title="Allow cdp proxy to send {}".format(erc[0]),
                    gas_limit=50000,
                )
                self.dapp.add_message_dialog(
                    "We must allow the CDP proxy to send {}".format(erc[0])
                )
                self.close()
                return

        # check to see if user actually has enough tokens to pay fee
        #debug(); pdb.set_trace()

        try:
            bal = [x['balance'] for x in self.dapp.node.erc20_balances if x['name'] == fee_denomination][0]
        except:
            self.dapp.add_message_dialog(
                "No {} balance found.  Is the token being tracked?".format(fee_denomination)
            )
            return

        if bal is None or bal < self.dapp.proportional_stability_fee( self.deposit_eth_value()):
            self.dapp.add_message_dialog(
                "You don't have enough {}.".format(fee_denomination)
            )
            return


        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.wipe(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address,
                self.dapp.cup_id, 
                self.deposit_eth_value() 
            ),
            title="Pay back {} DAI".format(
                self.deposit_eth_value_string()
            ),
            gas_limit=375013,
        )
        self.close()
 

    def projected_liquidation_price(self):
        try:
            liq_price = self.dapp.projected_liquidation_price(-1 * self.dapp.WAD * self.deposit_eth_value(), 0)
            if liq_price < Decimal(0):
                return "Undefined"
            return "{:f}".format(liq_price)[0:12] + " USD"
 
        except (decimal.InvalidOperation):
            return "Undefined"

    def projected_collateralization_ratio(self):
        try:
            proj_ratio = self.dapp.projected_collateralization_ratio(-1 * self.dapp.WAD * self.deposit_eth_value(), 0)
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
