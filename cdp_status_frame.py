from shadowlands.sl_dapp import SLFrame
from decimal import Decimal

from shadowlands.tui.debug import debug
from cdp_manager.lock_eth_frame import LockEthFrame
import pdb


class CDPStatusFrame(SLFrame):

    def drop(self):
        debug(); pdb.set_trace()

    def lock_eth_frame(self):
        #require_allowance(self, symbol, receiver_address, amount):
        #erc_contract.approve(receiver_address, amount * self.WAD)
        #debug(); pdb.set_trace()
        #self.dapp.lad
        if self.dapp.peth.allowance(self.dapp.peth.address, self.dapp.tub.address) < Decimal(2 ** 128 - 1):
            erc_contract.approveUnlimited(receiver_address)

        #    pass
        self.dapp.add_frame(LockEthFrame, 20, 50, title="Deposit Collateral")
        self.close()

    def initialize(self):
        #self.add_divider()
        
        self.add_label_quad("Liq. Price:", str(round(self.dapp.cdp_liquidation_price(self.dapp.cup_id), 4)) + " USD",
                            "Collat. Ratio:", str(round(self.dapp.cdp_collateralization_ratio(self.dapp.cup_id), 4)) + " %", add_divider=False)
        self.add_label_quad("Current Price:", str(round(self.dapp.ether_price(), 4)) + " USD",
                            "Minimum Ratio:", str(round(self.dapp.liquidation_ratio(), 4) * 100) + " %", add_divider=False)
        self.add_label_quad("Liq. penalty:", str(round(self.dapp.liquidation_penalty(), 4)) + " %",
                            "Stability Fee:", str(round(self.dapp.stability_fee(), 4)) + " %", add_divider=False)

        self.add_divider(draw_line=True)

        self.add_label("ETH Collateral")
        self.add_label_quad("Deposited:", str(round(self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " ETH",
                            "Max available:", str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id), 3)) + " ETH", add_divider=False)
        self.add_label_quad("", str(round(self.dapp.collateral_peth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " PETH",
                            "", str(round(self.dapp.peth_available_to_withdraw(self.dapp.cup_id), 3)) + " PETH", add_divider=False)
        self.add_label_quad("", str(round( Decimal(self.dapp.pip.eth_price() / self.dapp.WAD) * self.dapp.collateral_eth_value(self.dapp.cup_id) / self.dapp.WAD, 4)) +  " USD",
                            "", str(round(self.dapp.eth_available_to_withdraw(self.dapp.cup_id) * Decimal(self.dapp.pip.eth_price()) / self.dapp.WAD, 4)) + " USD", add_divider=True)
        self.add_ok_cancel_buttons(self.lock_eth_frame, self.close, "DEPOSIT", cancel_text="WITHDRAW", cancel_index=2)
        self.add_divider(draw_line=True)

        self.add_label("DAI Position")
        self.add_label_quad("Generated:", str(round(self.dapp.tub.tab(self.dapp.cup_id) / self.dapp.WAD, 2)) +  " DAI",
                            "Max available:", str(round(self.dapp.dai_available_to_generate(self.dapp.cup_id), 3)) + " DAI", add_divider=False)
        self.add_divider(draw_line=False)
        self.add_ok_cancel_buttons(self.close, self.close, "PAY BACK", cancel_text="GENERATE", cancel_index=2)
        self.add_divider(draw_line=False)
        self.add_divider(draw_line=False)

        self.add_button(self.close, "Quit", layout_distribution=[1, 1, 1, 1], layout_index=3)


