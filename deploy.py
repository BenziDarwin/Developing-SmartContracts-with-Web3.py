from solcx import install_solc
from solcx import compile_standard
import json
from web3 import Web3

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compiling Solidity

complied_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourcemap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print(complied_sol)

with open("compiled_code.json", "w") as file:
    json.dump(complied_sol, file)

# Get ByteCode
bytecode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi

abi = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(abi)

# Connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

chain_id = 5777
my_address = "0x3990a4b698F800C1199772cc5F217246510217bd"
my_private_key = "fb1abf9b187e64caeb43964f172bbd3b83dfb09ae8bbb977a8e2ccd933a84bcf"
