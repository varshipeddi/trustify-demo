import json
import time
from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Contract details
contract_address = "0xc945A6FA8a9043Aa35A4BA4e0089d05d4c3688fA"  # Update to match your deployed contract
compiled_contract_path = "../Smart Contract/build/contracts/ProductAuth.json"

# Load contract ABI
with open(compiled_contract_path, "r") as file:
    contract_json = json.load(file)
    contract_abi = contract_json["abi"]

# Connect to the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Event filter for ProductCreated
event_filter = contract.events.ProductCreated.create_filter(from_block='latest')

# Output file path
output_file_path = "product_data.json"

print("Listening for ProductCreated events...")

# Event listener loop
while True:
    try:
        events = event_filter.get_new_entries()
        if events:
            for event in events:
                # Safely extract and convert event details
                product_id = event['args']['productId']
                seller = event['args']['seller']
                price = event['args']['price']
                image_hash = event['args']['imageHash']

                # Log and save event data
                print(f"Detected ProductCreated event: Product ID={product_id}, Seller={seller}, Price={price}, Image Hash={image_hash}")

                product_data = {
                    "productId": str(product_id),
                    "seller": seller,
                    "price": str(price),
                    "imageHash": image_hash
                }

                # Open file in append mode with UTF-8 encoding
                with open(output_file_path, "a", encoding='utf-8') as file:
                    json.dump(product_data, file, indent=4)
                    file.write("\n")
                print(f"Saved product data to {output_file_path}")
        
        time.sleep(2)  # Poll interval
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)  # Prevent tight error loop