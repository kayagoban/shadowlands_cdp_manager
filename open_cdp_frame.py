from shadowlands.sl_dapp import SLFrame
from decimal import Decimal, InvalidOperation, DivisionByZero
import decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
from cdp_manager.cdp_status_frame import CDPStatusFrame
from cdp_manager.contracts.ds_proxy import DsProxy
import pdb



class OpenCDPFrame(SLFrame):

    def initialize(self):
 
        self.add_label("This address does not yet have a CDP registered.")
        self.eth_deposit_value = self.add_textbox("ETH to deposit:", default_value='')
        self.dai_withdrawal_value = self.add_textbox("DAI to generate:", default_value='')
        self.add_label("Current account balance (ETH):", add_divider=False)
        self.add_label(str(self.dapp.node.eth_balance)[0:8])
        self.add_label("Projected liquidation price:", add_divider=False)
        self.add_label(self.projected_liquidation_price)
        self.add_label("Projected collateralization ratio:", add_divider=False)
        self.add_label(self.projected_collateralization_ratio)

        self.add_label("Minimum ratio:", add_divider=False)
        self.add_label(str(self.dapp.liquidation_ratio * 100)[0:8] + " %")
        self.add_label("Liquidation Penalty:", add_divider=False)
        self.add_label(str(self.dapp.liquidation_penalty)[0:8] + " %")

        self.add_button_row(
            [
                ("Open CDP", self.open_cdp, 0),
                ("Back", self.close, 1)
            ]
        )

    def deposit_eth_value_string(self):
        return str(self.deposit_eth_value())

    def deposit_eth_value(self):
        try:
            return Decimal(self.eth_deposit_value() )
        except (TypeError, InvalidOperation):
            return Decimal(0.0)

    def dai_value_string(self):
        return str(self.dai_value())

    def dai_value(self):
        try:
            return Decimal(self.dai_withdrawal_value() )
        except (TypeError, InvalidOperation):
            return Decimal(0.0)


    def projected_collateralization_ratio(self):
        try:
            c_ratio = self.dapp.projected_collateralization_ratio(self.dai_value(),  self.deposit_eth_value())
            if c_ratio == 0:
                return "Undefined"
            return str(c_ratio / self.dapp.WAD)[0:12]
        except (decimal.DivisionByZero, decimal.InvalidOperation):
            return "Undefined"


    def projected_liquidation_price(self):
        try:
            l_price = self.dapp.projected_liquidation_price(self.dai_value(), self.deposit_eth_value())
            if l_price == 0:
                return "Undefined"
            return str(l_price * self.dapp.WAD)[0:12]
        except (decimal.InvalidOperation, decimal.DivisionByZero):
            return "Undefined"


    def open_cdp(self):
        # No current CDP open, but do we have a proxy ready for us?

        ds_proxy_address = self.dapp.proxy_registry.proxies(self.dapp.node.credstick.address)

        if ds_proxy_address is None:
            self.dapp.add_transaction_dialog(
                self.dapp.sai_proxy.createOpenLockAndDraw(
                    self.dapp.proxy_registry.address, 
                    self.dapp.tub.address, 
                    self.dai_withdrawal_value()
                ),
                title="Open CDP",
                gas_limit=980000,
                tx_value=Decimal(self.eth_deposit_value()),
            )
        else:
            ds_proxy = DsProxy(self.dapp.node, address=ds_proxy_address)
            self.dapp.add_transaction_dialog(
                ds_proxy.lock_and_draw(
                    self.dapp.sai_proxy.address,
                    self.dapp.tub.address, 
                    self.dai_withdrawal_value()
                ),
                title="Open CDP",
                gas_limit=980000,
                tx_value=Decimal(self.eth_deposit_value()),
            )

        self.close()
        

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


