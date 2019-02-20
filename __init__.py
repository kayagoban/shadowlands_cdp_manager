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
from cdp_manager.contracts.sai_pip import SaiPip
from cdp_manager.contracts.sai_pep import SaiPep
from cdp_manager.contracts.sai_pit import SaiPit
from cdp_manager.contracts.sai_top import SaiTop
from cdp_manager.contracts.sai_sin import SaiSin
from cdp_manager.contracts.sai_mom import SaiMom
from cdp_manager.contracts.sai_dad import SaiDad
from cdp_manager.contracts.sai_tub import SaiTub
from cdp_manager.contracts.sai_vox import SaiVox
from cdp_manager.contracts.sai_proxy import SaiProxy
from cdp_manager.contracts.ds_proxy import DsProxy
from cdp_manager.contracts.ds_proxy_factory import DsProxyFactory
from cdp_manager.contracts.maker_otc import MakerOtc
from cdp_manager.contracts.oasis_proxy import OasisProxy
from cdp_manager.contracts.proxy_registry import ProxyRegistry


class Dapp(SLDapp):
    def initialize(self):
        #self.name = None  # The full name given by the user
        #self.subdomain = None  # just the subdomain
        #self.domain = None # just the domain.eth
        #self.resolved_address = None 

        if self.node.network_name not in ["MainNet", "Kovan"]:
            self.add_message_dialog("This Dapp only functions on the Ethereum MainNet and Kovan")
            return

        #try:
        #    pass
        #except (ContractConfigError):
        #    self.add_message_dialog("Could not load the contracts for this Dapp.")
        #    return None

        self.add_frame(CDPStatusFrame, height=20, width=55, title="CDP info")


