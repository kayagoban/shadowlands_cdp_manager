from shadowlands.contract import Contract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],

class OasisProxy(Contract):

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
    MAINNET="0x793ebbe21607e4f04788f89c7a9b97320773ec59"
    KOVAN="0xee419971e63734fed782cfe49110b1544ae8a773"
    ABI='''
    [{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"payToken","type":"address"},{"name":"payAmt","type":"uint256"},{"name":"wethToken","type":"address"},{"name":"minBuyAmt","type":"uint256"}],"name":"sellAllAmountBuyEth","outputs":[{"name":"wethAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"payToken","type":"address"},{"name":"payAmt","type":"uint256"},{"name":"buyToken","type":"address"},{"name":"minBuyAmt","type":"uint256"}],"name":"sellAllAmount","outputs":[{"name":"buyAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"buyToken","type":"address"},{"name":"buyAmt","type":"uint256"},{"name":"payToken","type":"address"},{"name":"maxPayAmt","type":"uint256"}],"name":"buyAllAmount","outputs":[{"name":"payAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"wethAmt","type":"uint256"},{"name":"payToken","type":"address"},{"name":"maxPayAmt","type":"uint256"}],"name":"createAndBuyAllAmountBuyEth","outputs":[{"name":"proxy","type":"address"},{"name":"payAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"payToken","type":"address"},{"name":"payAmt","type":"uint256"},{"name":"minBuyAmt","type":"uint256"}],"name":"createAndSellAllAmountBuyEth","outputs":[{"name":"proxy","type":"address"},{"name":"wethAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"buyToken","type":"address"},{"name":"buyAmt","type":"uint256"}],"name":"createAndBuyAllAmountPayEth","outputs":[{"name":"proxy","type":"address"},{"name":"wethAmt","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"buyToken","type":"address"},{"name":"minBuyAmt","type":"uint256"}],"name":"createAndSellAllAmountPayEth","outputs":[{"name":"proxy","type":"address"},{"name":"buyAmt","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"buyToken","type":"address"},{"name":"buyAmt","type":"uint256"},{"name":"payToken","type":"address"},{"name":"maxPayAmt","type":"uint256"}],"name":"createAndBuyAllAmount","outputs":[{"name":"proxy","type":"address"},{"name":"payAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"buyToken","type":"address"},{"name":"buyAmt","type":"uint256"},{"name":"wethToken","type":"address"}],"name":"buyAllAmountPayEth","outputs":[{"name":"wethAmt","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"factory","type":"address"},{"name":"otc","type":"address"},{"name":"payToken","type":"address"},{"name":"payAmt","type":"uint256"},{"name":"buyToken","type":"address"},{"name":"minBuyAmt","type":"uint256"}],"name":"createAndSellAllAmount","outputs":[{"name":"proxy","type":"address"},{"name":"buyAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"wethToken","type":"address"},{"name":"buyToken","type":"address"},{"name":"minBuyAmt","type":"uint256"}],"name":"sellAllAmountPayEth","outputs":[{"name":"buyAmt","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"otc","type":"address"},{"name":"wethToken","type":"address"},{"name":"wethAmt","type":"uint256"},{"name":"payToken","type":"address"},{"name":"maxPayAmt","type":"uint256"}],"name":"buyAllAmountBuyEth","outputs":[{"name":"payAmt","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"wethToken_","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]
'''

 
