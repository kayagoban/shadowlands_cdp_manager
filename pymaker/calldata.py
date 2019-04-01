from cdp_manager.pymaker.util import synchronize, bytes_to_hexstring
from web3.utils.contracts import get_function_info, encode_abi
import re
from web3 import Web3
from shadowlands.tui.debug import debug
import pdb

class Calldata:
    """Represents Ethereum calldata.

    Attributes:
        value: Calldata as either a string starting with `0x`, or as bytes.
    """
    def __init__(self, value):
        if isinstance(value, str):
            assert(value.startswith('0x'))
            self.value = value

        elif isinstance(value, bytes):
            self.value = bytes_to_hexstring(value)

        else:
            raise Exception("Unable to create calldata from '{}'".format(value))

    @classmethod
    def from_signature(cls, fn_sign: str, fn_args: list):
        """ Allow to create a `Calldata` from a function signature and a list of arguments.

        :param fn_sign: the function signature ie. "function(uint256,address)"
        :param fn_args: arguments to the function ie. [123, "0x00...00"]
        :return:
        """
        assert isinstance(fn_sign, str)
        assert isinstance(fn_args, list)

        fn_split = re.split('[(),]', fn_sign)
        fn_name = fn_split[0]
        fn_args_type = [{"type": type} for type in fn_split[1:] if type]

        #debug(); pdb.set_trace()

        fn_abi = {"type": "function", "name": fn_name, "inputs": fn_args_type}
        fn_abi, fn_selector, fn_arguments = get_function_info("test", fn_abi=fn_abi, args=fn_args)

        calldata = encode_abi(Web3, fn_abi, fn_arguments, fn_selector)

        return cls(calldata)

    def as_bytes(self) -> bytes:
        """Return the calldata as a byte array."""
        return bytes.fromhex(self.value.replace('0x', ''))

    def __str__(self):
        return "{}".format(self.value)

    def __repr__(self):
        return "Calldata('{}')".format(self.value)

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, other):
        assert(isinstance(other, Calldata))
        return self.value == other.value
