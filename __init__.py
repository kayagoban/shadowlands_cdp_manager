from shadowlands.sl_dapp import SLDapp, SLFrame, ExitDapp

#import random, string
#from datetime import datetime, timedelta

from shadowlands.contract import ContractConfigError
from shadowlands.tui.debug import debug
import pdb

#from ens_manager.contracts.ens_resolver import EnsResolver
#from ens_manager.contracts.ens_auction import EnsAuction
#from ens_manager.contracts.ens_registry import EnsRegistry
#from ens_manager.contracts.ens_reverse_resolver import EnsReverseResolver

#from ens_manager.status_frame import ENSStatusFrame



class Dapp(SLDapp):
    def initialize(self):
        #self.name = None  # The full name given by the user
        #self.subdomain = None  # just the subdomain
        #self.domain = None # just the domain.eth
        #self.resolved_address = None 

        if self.node.network_name != "MainNet":
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet")
            return

        #try:
        #    pass
        #except (ContractConfigError):
        #    self.add_message_dialog("Could not load the contracts for this Dapp.")
        #    return None

        self.add_frame(CDPStatusFrame, height=20, width=55, title="CDP info")


