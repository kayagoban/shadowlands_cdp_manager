from shadowlands.sl_contract import SLContract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

class SaiPit(SLContract):

    MAINNET="0x69076e44a9c70a67d5b79d95795aba299083c275"
    KOVAN="0xbd747742b0f1f9791d3e6b85f8797a0cf4fbf10b"
    ABI='''[{"constant":false,"inputs":[{"name":"gem","type":"address"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]
'''

 
