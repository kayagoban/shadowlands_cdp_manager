from shadowlands.contract import Contract
from hexbytes import HexBytes
from eth_utils import decode_hex, to_checksum_address

from shadowlands.tui.debug import debug
import pdb
from cdp_manager.pymaker.calldata import Calldata
from decimal import Decimal

# [contracts.SAI_PIT]: [
#      { version: 1, address: addresses.PIT, abi: abis.daiV1.pit }
# ],




class DsProxy(Contract):

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

    def close(self):
        calldata = Calldata.from_signature(
            "function(bytes32)",
            [
                self.bytes32(cup_id),
            ]
        )
        payload = calldata.as_bytes()
        fn = self.functions.execute(tub_addr, payload)
        return fn

 
    def draw(self, proxy_addr, tub_addr, cup_id, amount):
        calldata = Calldata.from_signature(
	    "draw(address,bytes32,uint256)",
	    [
		tub_addr,
		self.bytes32(cup_id),
                self.toWei(amount, 'ether')
            ]
	)
        payload = calldata.as_bytes()

        fn = self.functions.execute(proxy_addr, payload)
        return fn

    def shut(self, proxy_addr, tub_addr, cup_id):
        calldata = Calldata.from_signature(
	    "shut(address,bytes32)",
	    [
		tub_addr,
		self.bytes32(cup_id)
            ]
	)
        payload = calldata.as_bytes()
        fn = self.functions.execute(proxy_addr, payload)
        return fn



    def give(self, proxy_addr, tub_addr, cup_id, target):
        calldata = Calldata.from_signature(
	    "give(address,bytes32,address)",
	    [
		tub_addr,
		self.bytes32(cup_id),
                target 
            ]
	)
        payload = calldata.as_bytes()
        fn = self.functions.execute(proxy_addr, payload)
        return fn

    def wipe(self, proxy_addr, tub_addr, cup_id, amount):
        calldata = Calldata.from_signature(
	    "wipe(address,bytes32,uint256)",
	    [
		tub_addr,
		self.bytes32(cup_id),
                self.toWei(amount, 'ether')
            ]
	)
        payload = calldata.as_bytes()
        #debug(); pdb.set_trace()
        fn = self.functions.execute(proxy_addr, payload)
        return fn


	

    def free(self, proxy_addr, tub_addr, cup_id, amount):

        calldata = Calldata.from_signature(
	    "free(address,bytes32,uint256)",
	    [
		tub_addr,
		self.bytes32(cup_id),
                self.toWei(amount, 'ether')
            ]
	)
        payload = calldata.as_bytes()

        fn = self.functions.execute(proxy_addr, payload)
        return fn

    def lock_and_draw(self, proxy_addr, registry_addr, tub_addr, amount):
        calldata = Calldata.from_signature(
	    "LockAndDraw(address,address,uint256)",
	    [
                registry_addr,
		tub_addr,
                self.toWei(amount, 'ether')
            ]
	)
        payload = calldata.as_bytes()

        fn = self.functions.execute(proxy_addr, payload)
        return fn


    def lock(self, proxy_addr, tub_addr, cup_id):
        calldata = Calldata.from_signature(
	    "lock(address,bytes32)",
	    [
		tub_addr,
		self.bytes32(cup_id)
            ]
	)
        payload = calldata.as_bytes()

        fn = self.functions.execute(proxy_addr, payload)
        return fn

    ABI='''
[
   {
      "constant":false,
      "inputs":[
         {
            "name":"owner_",
            "type":"address"
         }
      ],
      "name":"setOwner",
      "outputs":[

      ],
      "payable":false,
      "stateMutability":"nonpayable",
      "type":"function"
   },
   {
      "constant":false,
      "inputs":[
         {
            "name":"_target",
            "type":"address"
         },
         {
            "name":"_data",
            "type":"bytes"
         }
      ],
      "name":"execute",
      "outputs":[
         {
            "name":"response",
            "type":"bytes"
         }
      ],
      "payable":true,
      "stateMutability":"payable",
      "type":"function"
   },
   {
      "constant":true,
      "inputs":[

      ],
      "name":"cache",
      "outputs":[
         {
            "name":"",
            "type":"address"
         }
      ],
      "payable":false,
      "stateMutability":"view",
      "type":"function"
   },
   {
      "constant":false,
      "inputs":[
         {
            "name":"authority_",
            "type":"address"
         }
      ],
      "name":"setAuthority",
      "outputs":[

      ],
      "payable":false,
      "stateMutability":"nonpayable",
      "type":"function"
   },
   {
      "constant":true,
      "inputs":[

      ],
      "name":"owner",
      "outputs":[
         {
            "name":"",
            "type":"address"
         }
      ],
      "payable":false,
      "stateMutability":"view",
      "type":"function"
   },
   {
      "constant":false,
      "inputs":[
         {
            "name":"_cacheAddr",
            "type":"address"
         }
      ],
      "name":"setCache",
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "stateMutability":"nonpayable",
      "type":"function"
   },
   {
      "constant":true,
      "inputs":[

      ],
      "name":"authority",
      "outputs":[
         {
            "name":"",
            "type":"address"
         }
      ],
      "payable":false,
      "stateMutability":"view",
      "type":"function"
   },
   {
      "inputs":[
         {
            "name":"_cacheAddr",
            "type":"address"
         }
      ],
      "payable":false,
      "stateMutability":"nonpayable",
      "type":"constructor"
   },
   {
      "payable":true,
      "stateMutability":"payable",
      "type":"fallback"
   },
   {
      "anonymous":true,
      "inputs":[
         {
            "indexed":true,
            "name":"sig",
            "type":"bytes4"
         },
         {
            "indexed":true,
            "name":"guy",
            "type":"address"
         },
         {
            "indexed":true,
            "name":"foo",
            "type":"bytes32"
         },
         {
            "indexed":true,
            "name":"bar",
            "type":"bytes32"
         },
         {
            "indexed":false,
            "name":"wad",
            "type":"uint256"
         },
         {
            "indexed":false,
            "name":"fax",
            "type":"bytes"
         }
      ],
      "name":"LogNote",
      "type":"event"
   },
   {
      "anonymous":false,
      "inputs":[
         {
            "indexed":true,
            "name":"authority",
            "type":"address"
         }
      ],
      "name":"LogSetAuthority",
      "type":"event"
   },
   {
      "anonymous":false,
      "inputs":[
         {
            "indexed":true,
            "name":"owner",
            "type":"address"
         }
      ],
      "name":"LogSetOwner",
      "type":"event"
   }
]
'''

#  [{"constant":false,"inputs":[{"name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_target","type":"address"},{"name":"_data","type":"bytes"}],"name":"execute","outputs":[{"name":"response","type":"bytes"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"_code","type":"bytes"},{"name":"_data","type":"bytes"}],"name":"execute","outputs":[{"name":"target","type":"address"},{"name":"response","type":"bytes"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"cache","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_cacheAddr","type":"address"}],"name":"setCache","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_cacheAddr","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":true,"inputs":[{"indexed":true,"name":"sig","type":"bytes4"},{"indexed":true,"name":"guy","type":"address"},{"indexed":true,"name":"foo","type":"bytes32"},{"indexed":true,"name":"bar","type":"bytes32"},{"indexed":false,"name":"wad","type":"uint256"},{"indexed":false,"name":"fax","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"}]

 
