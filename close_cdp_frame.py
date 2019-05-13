from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

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

        self.add_label_pair("Stability fee in MKR:", str(self.dapp.mkr_cdp_stability_fee)[0:18])

        #self.stability_fee_options = [
        #    ("MKR", 0),
        #    ("DAI", 1)
        #]

        #self.stability_fee_denomination = self.add_radiobuttons(self.stability_fee_options, label="Pay stability fee in:")

        
        #self.add_divider()

        self.add_ok_cancel_buttons(self.close_cdp_choice, cancel_fn=self.close, ok_text="Close CDP", cancel_text="Cancel")


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
            gas_limit=500000,
        )
        self.close()

        #self.add_divider(draw_line=True)
        #self.eth_deposit_value = self.add_textbox("ETH to deposit:", default_value='1')
        #self.add_divider(draw_line=True)
        #self.dai_withdrawal_value = self.add_textbox("DAI to generate:", default_value='1')
        #self.add_ok_cancel_buttons(self.open_cdp, ok_text="Open CDP")

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


