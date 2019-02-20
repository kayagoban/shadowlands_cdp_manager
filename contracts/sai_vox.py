from shadowlands.contract import Contract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],

class SaiVox(Contract):

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
    MAINNET="0x9b0f70df76165442ca6092939132bbaea77f2d7a"
    KOVAN="0xbb4339c0ab5b1d9f14bd6e3426444a1e9d86a1d9"
    ABI='''[{"constant":false,"inputs":[],"name":"prod","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"era","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"how","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"par","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"tell","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"way","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"param","type":"bytes32"},{"name":"val","type":"uint256"}],"name":"mold","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"fix","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"tune","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tau","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"par_","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":true,"inputs":[{"indexed":true,"name":"sig","type":"bytes4"},{"indexed":true,"name":"guy","type":"address"},{"indexed":true,"name":"foo","type":"bytes32"},{"indexed":true,"name":"bar","type":"bytes32"},{"indexed":false,"name":"wad","type":"uint256"},{"indexed":false,"name":"fax","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"}]
'''

 
