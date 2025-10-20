import json
from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection to Ganache
if w3.is_connected():
    print("Connected to Ganache!")
else:
    raise Exception("Failed to connect to Ganache. Ensure Ganache is running.")

# Path to compiled contract JSON file
compiled_contract_path = "../Smart Contract/build/contracts/ProductAuth.json"

# Load contract ABI and bytecode
with open(compiled_contract_path, "r") as file:
    contract_json = json.load(file)
    contract_abi = contract_json["abi"]
    contract_bytecode = contract_json["bytecode"]

# Deploy the contract
contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Use the first account in Ganache as the deployer
deployer_account = w3.eth.accounts[0]

# Build the deployment transaction
tx_hash = contract.constructor().transact({
    "from": deployer_account,
    "gas": 5000000,  # Increase gas limit
    "gasPrice": w3.to_wei("20", "gwei")  # Explicit gas price
})

print(tx_hash)

# Wait for the transaction to be mined
print("Deploying contract...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Get the deployed contract address
contract_address = tx_receipt.contractAddress
print("Contract deployed successfully!")
print("Contract Address:", contract_address)
