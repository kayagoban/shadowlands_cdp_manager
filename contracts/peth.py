from shadowlands.sl_contract.erc20 import Erc20
from hexbytes import HexBytes
from eth_utils import decode_hex

from shadowlands.tui.debug import debug
import pdb

class Peth(Erc20):
    MAINNET="0xf53ad2c6851052a81b42133467480961b2321c09"
    KOVAN='0xf4d791139cE033Ad35DB2B2201435fAd668B1b64'
 
    def to_sol_addr(self, address):
        return decode_hex(address.replace('0x',''))

    def to_bytes_32(self, value):
        return value.to_bytes(32, byteorder='big')

    def totalSupply(self):
        return self.functions.totalSupply().call()

    def allowance(self, src, target):
        debug(); pdb.set_trace()
        response = self.functions.allowance(self.to_sol_addr(src), self.to_sol_addr(target)).call()
        return response


    # transactions

    def approveUnlimited(self, target):
        self.approve(target, -1)

    def approve(self, target, amount):
        debug(); pdb.set_trace()
        fn = self.functions.approve(solf.to_sol_addr(target), int(amount))


   
