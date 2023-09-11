import re

from web3 import Web3
from eth_abi import encode


# Web3.toChecksumAddress() "Returns the given address with an EIP55 checksum."
# Web3.solidityKeccak "Returns the Keccak-256 of the given value"
pattern = re.compile("\((.*)\)")


def calc_create_address(address, nonce):
    if nonce == 0x00:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8'],
                                [0xd6, 0x94, address, 0x80])[12:].hex()
    elif nonce <= 0x7f:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8'],
                                [0xd6, 0x94, address, nonce])[12:].hex()
    elif nonce <= 0xff:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8', 'uint8'],
                                [0xd7, 0x94, address, 0x81, nonce])[12:].hex()
    elif nonce <= 0xffff:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8', 'uint16'],
                                [0xd8, 0x94, address, 0x82, nonce])[12:].hex()
    elif nonce <= 0xffffff:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8', 'uint24'],
                                [0xd9, 0x94, address, 0x83, nonce])[12:].hex()
    else:
        data = Web3.solidity_keccak(['uint8', 'uint8', 'address', 'uint8', 'uint32'],
                                [0xda, 0x94, address, 0x84, nonce])[12:].hex()
    return Web3.to_checksum_address(data)


def calc_create2_address(address, salt, code):
    code_hash = Web3.solidity_keccak(['bytes'], [code])
    data = Web3.solidity_keccak(['uint8', 'address', 'bytes32', 'bytes32'],
                            [0xff, address, salt, code_hash])[12:].hex()
    return Web3.to_checksum_address(data)


def calc_func_selector(sig):
    func_selector: bytes = Web3.solidity_keccak(['string'], [sig])[:4]
    return func_selector


def calc_call_data(sig, *, args=[]):
    types = pattern.findall(sig)[0].split(',')
    if types == ['']:
        types = []
    func_selector: bytes = calc_func_selector(sig)
    data: bytes = encode(types, args)
    return "0x" + (func_selector + data).hex()


# Test
if __name__ == '__main__':
    addr1 = calc_create_address('0x9Fb798AC1d3Dce899D7E0047DdA5ed4598A6911A', 0)
    assert addr1 == '0x47d3EEA4b1d8dEA7CA26703108Ae3423817bf47E'

    code = '0x6080604052348015600f57600080fd5b506706f05b59d3b200004710602c576000805460ff191660011790555b60838061' \
        '003a6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c8063890eba6814602d575b' \
        '600080fd5b60005460399060ff1681565b604051901515815260200160405180910390f3fea2646970667358221220c0afce' \
        '3a78fcc60fe5cb042db9c8cae10e646b3fcd2f905fa125145eebdf049864736f6c63430008110033'
    salt = Web3.solidity_keccak(['string'], ['HGAME 2023'])
    addr2 = calc_create2_address('0x47d3EEA4b1d8dEA7CA26703108Ae3423817bf47E', salt, code)
    assert addr2 == '0x4321D637fF29e9ee17Fe0c1B5c9745b049d61b56'

    assert calc_func_selector("setTime(uint256)").hex() == '0x3beb26c4'
    assert calc_call_data("setTime(uint256)", args=[1]) == \
        "0x3beb26c40000000000000000000000000000000000000000000000000000000000000001"

    assert calc_call_data("poc()") == "0x2cce6b01"
