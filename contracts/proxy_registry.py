from shadowlands.sl_contract import SLContract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],

NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
class ProxyRegistry(SLContract):

    def proxies(self, address):
        result = self.functions.proxies(address).call()
        if result == NULL_ADDRESS:
            return None
        else:
            return result

    def build(self):
        return self.functions.build()

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
    MAINNET="0x4678f0a6958e4D2Bc4F1BAF7Bc52E8F3564f3fE4"
    KOVAN="0xe11e3b391f7e8bc47247866af32af67dd58dc800"
    ABI='''
    [{"constant":false,"inputs":[],"name":"build","outputs":[{"name":"proxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"proxies","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"owner","type":"address"}],"name":"build","outputs":[{"name":"proxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"factory_","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]
'''

 
