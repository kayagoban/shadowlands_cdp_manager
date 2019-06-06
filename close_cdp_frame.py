from shadowlands.sl_dapp import SLFrame
from decimal import Decimal, DivisionByZero, InvalidOperation, DivisionUndefined

from cached_property import cached_property
from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
#from cdp_manager.cdp_status_frame import CDPStatusFrame
import pdb



class CloseCDPFrame(SLFrame):

    def initialize(self):

        self.add_label_row([
            ("Outstanding debt:", 0),
            ("{:f}".format( self.debt_value())[0:16] + " DAI", 1)
        ],
            add_divider=False,
            layout=[4, 4]
        )

        self.add_label_with_button(
            self.your_dai, 
            "Get DAI", 
            self.dai_uniswap_frame
        )

        self.add_label_row([
            ("Stability Fee:", 0),
            (self.stability_fee, 1)
        ],
            add_divider=False,
            layout=[4, 4]
        )

        self.add_label_with_button(
            self.your_mkr, 
            "Get MKR", 
            self.mkr_uniswap_frame
        )

        self.add_button_row([
            ("Close CDP", self.close_cdp_choice, 0),
            ("Cancel", self.close, 3)
        ])

    @cached_property
    def your_dai(self):
        return "Your DAI: {:f}".format(self.dapp.dai.my_balance() / 10 ** 18)[:22]

    @cached_property
    def your_mkr(self):
        return "Your MKR: {:f}".format(self.dapp.mkr.my_balance() / 10 ** 18)[:22]


    def debt_value(self):
        try:
            debt = self.dapp.debt_value / self.dapp.WAD
        except (InvalidOperation, DivisionUndefined):
            return Decimal(0)

        return debt
                                   
    def dai_uniswap_frame(self):
        self.dapp.add_uniswap_frame(self.dapp.dai.address, action='buy', buy_amount=self.debt_value())

    def mkr_uniswap_frame(self):
        self.dapp.add_uniswap_frame(self.dapp.mkr.address, action='buy', buy_amount=self.uniswap_to_buy_mkr_value())

    def uniswap_to_buy_mkr_value(self):
        sfee = self.dapp.cdp_stability_fee / self.dapp.WAD
        return sfee + sfee * Decimal(0.01)

    def stability_fee(self):
        try:
            fee = self.uniswap_to_buy_mkr_value()

            if fee == Decimal('0'):
                return "0"

            return str(fee)[0:10]
        except DivisionByZero:
            return ""



    def close_cdp_choice(self):

        # check for mkr or dai stability fee choice

        # check to see if we need to unlock
        fee_denomination = 'MKR'
        fee_erc20_contract = self.dapp.mkr

        allowance = fee_erc20_contract.allowance(
            self.dapp.node.credstick.address, 
            self.dapp.ds_proxy.address
        )

        if allowance < self.dapp.mkr_cdp_stability_fee:
            self.dapp.add_transaction_dialog(
                fee_erc20_contract.approve(
                    self.dapp.ds_proxy.address, 
                    self.dapp.MAX_WEI
                ),
                title="Allow cdp proxy to send {}".format(fee_denomination),
                gas_limit=50000,
            )
            self.dapp.add_message_dialog(
                "First we must allow the CDP proxy to send {}".format(fee_denomination)
            )
            self.close()
            return




        # unlock if needed - and then back to this frame
        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.shut(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address,
                self.dapp.cup_id
            ),
            title="Close CDP",
            gas_limit=700000,
        )
        self.close()

