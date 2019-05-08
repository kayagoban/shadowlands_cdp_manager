from shadowlands.sl_dapp import SLFrame
from cdp_manager.cdp_status_frame import CDPStatusFrame


class CupIDPromptFrame(SLFrame):
    def initialize(self):
        self.add_label("Maker's Web API could not be contacted.")
        self.add_label("Please enter the ID number of the CDP you want to control")
        cdp_id_value = self.add_textbox("CDP ID:")
        self.add_button_row([
            ("Examine CDP", self.examine_choice, 2),
            ("Exit", self.close, 3)
        ])

    def examine_choice(self):
        self.dapp.cup_id = int(cdp_id_value())
        self.add_frame(CDPStatusFrame, height=22, width=70, title="CDP {} info".format(self.dapp.cup_id))
