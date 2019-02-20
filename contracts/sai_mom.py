from shadowlands.contract import Contract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],

class SaiMom(Contract):

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
    MAINNET="0xf2c5369cffb8ea6284452b0326e326dbfdcb867c"
    KOVAN="0x72ee9496b0867dfe5e8b280254da55e51e34d27b"
    ABI='''[{"constant":false,"inputs":[{"name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"setTubGap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"setTapGap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setTax","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"tub","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"setCap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"vox","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setFee","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setMat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pip_","type":"address"}],"name":"setPip","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setHow","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setAxe","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"ray","type":"uint256"}],"name":"setWay","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"vox_","type":"address"}],"name":"setVox","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pep_","type":"address"}],"name":"setPep","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"tap","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"tub_","type":"address"},{"name":"tap_","type":"address"},{"name":"vox_","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":true,"inputs":[{"indexed":true,"name":"sig","type":"bytes4"},{"indexed":true,"name":"guy","type":"address"},{"indexed":true,"name":"foo","type":"bytes32"},{"indexed":true,"name":"bar","type":"bytes32"},{"indexed":false,"name":"wad","type":"uint256"},{"indexed":false,"name":"fax","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"}]
'''

 
