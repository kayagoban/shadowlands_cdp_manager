from shadowlands.contract import Contract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],

class SaiPit(Contract):

#    def resolve(self, name):
#        if not name.endswith(".eth"):
#            name += '.eth'
#        _namehash = namehash(name)
#        return self.functions.addr(_namehash).call()
# 
#
#    def set_address(self, name, address_target):
#        if not name.endswith(".eth"):
#            name += '.eth'
#
#        _namehash = namehash(name)
#
#        fn = self._contract.functions.setAddr(_namehash, HexBytes(address_target))
#        return fn
 
    MAINNET="0x69076e44a9c70a67d5b79d95795aba299083c275"
    KOVAN="0xbd747742b0f1f9791d3e6b85f8797a0cf4fbf10b"
    ABI='''[{"constant":false,"inputs":[{"name":"gem","type":"address"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]
'''

 
