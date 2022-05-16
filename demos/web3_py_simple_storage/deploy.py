from itertools import chain
from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()  # this will load the .env and load it into the script

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile Our Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/b207dd5e0c6345b59cff8cbff1af0e9a")
)
chain_id = 4
my_address = "0x4772D446dc740bb8B6Cf0C8B544d14e4D26F7085"
private_key = os.getenv("PRIVATE_KEY")
print("Private key: ")
print(private_key)
# Whenever I import a private key in Python I need to add 0x to the beginning to significy it is hex.

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction (nonce is like the transaction count)
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
print("Deploying contract...")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)
# print(transaction)
signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)  # sign
# send signed transaction to the block chain
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(
    tx_hash
)  # get receipt (this is so I can interact with it on the blockchain)
print("Contract deployed!")
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Types of method calls
# 1. Call -> Simulate making the call and getting a return value (this is more for testing).
# 2. Transact -> Actually make a state change on the blockchain.
print(simple_storage.functions.retrieve().call())
print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
# print(simple_storage.functions.store(15).call())
print("Contract updated!")

print(simple_storage.functions.retrieve().call())
