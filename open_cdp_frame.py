from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
import pdb


#debug(); pdb.set_trace()

class OpenCDPFrame(SLFrame):

    def initialize(self):
        self.add_divider()
        self.add_label("This address does not yet have a CDP registered")
        self.add_ok_cancel_buttons(self.open_cdp, ok_text="Open CDP")

    def open_cdp(self):
        self.dapp.add_transaction_wait_dialog(
            lambda: self.dapp.tub.open(),
            "Waiting for the Tx to be mined...",
            title="Open CDP",
            gas_limit=53159,
            receipt_proc=self.process_receipt
        )

    def process_receipt(self, rxo):
        id_hex = rxo.logs[1]['data']
        self.dapp.cup_id = int(id_hex, 16)

        
    # open new cdp
    
    # send 'open' to tub
    # const txo = await tubContract.open({ promise });

    # parse cdp ID from tx log 
    #   this.id = parseInt(txo.receipt.logs[1].data, 16);


