from solcx import install_solc
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
my_private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(simpleStorage)

# Get transaction count
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# Build a transaction
print("Deploying contract...")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)

# Sign a transaction

signed_txn = w3.eth.account.sign_transaction(transaction, my_private_key)
# print(signed_txn)

# Send a transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# print(txn_hash)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Contract Deployed!")
# print(txn_receipt)

# When working with a contract, you will need the contract addres and the contract abi

simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# Transact -> State change to the contract
# simple_storage.functions.giveValue(34).call()

# Build the transaction
print("Changing Favorite number...")
store_transaction = simple_storage.functions.giveValue(20).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

# Sign the transaction
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, my_private_key
)
print("Favorite number changed!")

# Send the transaction

send_store_txn = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)


# Call -> No state change to the Contract
print(simple_storage.functions.showValue().call())
