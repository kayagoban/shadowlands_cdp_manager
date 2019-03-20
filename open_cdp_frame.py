from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
import pdb


class OpenCDPFrame(SLFrame):

    def drop(self):
        debug(); pdb.set_trace()

    def initialize(self):
        self.add_divider()
        self.add_label("This address does not yet have a CDP registered")
        self.add_ok_cancel_buttons(self.open_cdp, ok_text="Open CDP")

    def open_cdp(self):
        self.dapp.add_transaction_dialog(
            tx_fn=lambda: self.dapp.tub.open(),
            title="Open CDP",
            gas_limit=55000
        )

        

        
    # open new cdp
    
    # send 'open' to tub
    # const txo = await tubContract.open({ promise });

    # parse cdp ID from tx log 
    #   this.id = parseInt(txo.receipt.logs[1].data, 16);


