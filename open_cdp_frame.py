from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
from cdp_manager.cdp_status_frame import CDPStatusFrame
import pdb



class OpenCDPFrame(SLFrame):

    def initialize(self):
        self.add_divider()
        self.add_label("This address does not yet have a CDP registered.")
        self.add_divider(draw_line=True)
        self.eth_deposit_value = self.add_textbox("ETH to deposit:", default_value='1')
        self.add_divider(draw_line=True)
        self.dai_withdrawal_value = self.add_textbox("DAI to generate:", default_value='1')
        self.add_ok_cancel_buttons(self.open_cdp, ok_text="Open CDP")

    def open_cdp(self):
        #try:
        self.dapp.add_transaction_wait_dialog(
            lambda: self.dapp.sai_proxy.createOpenLockAndDraw(
                self.dapp.proxy_registry.address, 
                self.dapp.tub.address, 
                self.dai_withdrawal_value()
            ),
            wait_message="Wait for the receipt",
            title="Open CDP",
            gas_limit=968650,
            tx_value=Decimal(self.eth_deposit_value()),
            receipt_proc=self.process_receipt
        )

        #self.dapp.add_transaction_dialog(
        #    self.dapp.sai_proxy.createOpenLockAndDraw(
        #        self.dapp.proxy_registry.address, 
        #        self.dapp.tub.address, 
        #        self.dai_withdrawal_value()
        #    ),
        #    title="Open CDP",
        #    gas_limit=968650,
        #    tx_value=Decimal(self.eth_deposit_value())
        #)

        self.close()
        #except:
        #    self.dapp.add_message_dialog("An error occured opening your CDP")

    def process_receipt(self, rxo):
        #debug(); pdb.set_trace()

        if rxo.blockNumber == None:
            # failure
            self.dapp.add_message_dialog("Transaction {} failed.".format(rxo.transactionHash.hex()))

        #id_hex = rxo.logs[1]['data']
        #self.dapp.cup_id = int(id_hex, 16)

        self.dapp.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.dapp.cup_id))
        self.dapp.add_message_dialog("New CDP Created.")

        
    # open new cdp
    
    # send 'open' to tub
    # const txo = await tubContract.open({ promise });

    # parse cdp ID from tx log 
    #   this.id = parseInt(txo.receipt.logs[1].data, 16);


