from shadowlands.sl_contract import SLContract
from hexbytes import HexBytes

from shadowlands.tui.debug import debug
import pdb

class DsProxyFactory(SLContract):

    MAINNET="0xa26e15c895efc0616177b7c1e7270a4c7d51c997"
    KOVAN="0xe11e3b391f7e8bc47247866af32af67dd58dc800"
    ABI='''
    [{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isProxy","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"cache","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"build","outputs":[{"name":"proxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"owner","type":"address"}],"name":"build","outputs":[{"name":"proxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"},{"indexed":true,"name":"owner","type":"address"},{"indexed":false,"name":"proxy","type":"address"},{"indexed":false,"name":"cache","type":"address"}],"name":"Created","type":"event"}]
'''

 
