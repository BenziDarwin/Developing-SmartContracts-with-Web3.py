from solcx import install_solc
from solcx import compile_standard
import json

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
