import json
from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Path to the compiled contract JSON file (replace with your actual path)
compiled_contract_path = "../Smart Contract/build/contracts/ProductAuth.json"  # Truffle output path

# Load contract ABI and bytecode
with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # Load the compiled JSON file
    contract_abi = contract_json["abi"]
    contract_bytecode = contract_json["bytecode"]

# Check connection to Ganache
if w3.isConnected():
    print("Connected to Ganache!")
else:
    print("Failed to connect to Ganache!")

# Deploy the contract
contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Build transaction
tx_hash = contract.constructor().transact({
    "from": w3.eth.accounts[0],  # Use the first Ganache account
    "gas": 3000000
})

# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get contract address
contract_address = tx_receipt.contractAddress
print("Contract deployed at:", contract_address)
