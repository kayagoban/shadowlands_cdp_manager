from shadowlands.sl_dapp import SLFrame
from decimal import Decimal, DivisionByZero

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
#from cdp_manager.cdp_status_frame import CDPStatusFrame
import pdb



class CloseCDPFrame(SLFrame):

    def initialize(self):
        info_text = [
            "Closing your CDP requires paying back your",
            "outstanding Dai debt, as well as the ",
            "accumulated stability fee, in MKR."
        ]

        for i in info_text:
            self.add_label(i, add_divider=False)

        self.add_divider()

        self.add_label_pair("Outstanding DAI:", str(self.dapp.debt_value / self.dapp.WAD)[0:18])

        self.add_label_pair("Stability fee in MKR:", self.stability_fee)

        self.add_button_row([
            ("Close CDP", self.close_cdp_choice, 0),
            ("Cancel", self.close, 1)
        ])


    def stability_fee(self):
        try:
            fee = self.dapp.cdp_stability_fee / self.dapp.WAD

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

