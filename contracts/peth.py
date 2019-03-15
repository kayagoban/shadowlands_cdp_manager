from shadowlands.contract.erc20 import Erc20
from hexbytes import HexBytes
from eth_utils import decode_hex

from shadowlands.tui.debug import debug
import pdb

class Peth(Erc20):

    def totalSupply(self):
        return self.functions.totalSupply().call()

    def allowance(self, target, amount):
        src_addr = decode_hex( bidding_address.replace('0x','') )

        fn = self.functions.allowance(source, target) 


    MAINNET='0x9AeD7A25F2d928225e6fb2388055c7363aD6727b'
