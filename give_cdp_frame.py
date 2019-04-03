from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
#from cdp_manager.cdp_status_frame import CDPStatusFrame
import pdb


class GiveCDPFrame(SLFrame):

    def initialize(self):
        self.add_divider()
        self.recipient_addr_value = self.add_textbox("Transfer to:")
        self.add_button_row([
            ("Transfer", self.transfer_cdp, 2),
            ("Cancel", self.close, 3)
        ])

    def transfer_cdp(self):
        # validate address
        target =  self.dapp.proxy_registry.proxies(self.recipient_addr_value())

        # If there's no ds_proxy available, just give it to the address.
        if target is None:
            target = self.recipient_addr_value()

        self.dapp.add_transaction_dialog(
            self.dapp.ds_proxy.give(
                self.dapp.sai_proxy.address, 
                self.dapp.tub.address, 
                self.dapp.cup_id, 
                target
            ),
            title="Transfer CDP",
            gas_limit=55000
        )

        self.close()
