import streamlit as st
from PIL import Image
from web3 import Web3
import hashlib
import json
from tensorflow.keras.models import load_model
import tensorflow as tf

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Contract details
contract_address = "0xc945A6FA8a9043Aa35A4BA4e0089d05d4c3688fA"  # Replace with your deployed contract address
compiled_contract_path = "../Smart Contract/build/contracts/ProductAuth.json"  # Replace with your Truffle build path

# Load contract ABI
with open(compiled_contract_path, "r") as file:
    contract_json = json.load(file)
    contract_abi = contract_json["abi"]

# Connect to the deployed contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Load the trained model
model = load_model('C:/Users/phama/Downloads/Vaida_aimfall2024/CNN Model/real_vs_fake_vgg16_model.keras')

# Function to generate SHA-256 hash
def generate_image_hash(image):
    return hashlib.sha256(image.read()).hexdigest()

# Function to preprocess and predict image
def predict_image(image):
    img = Image.open(image).resize((150, 150))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = tf.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return prediction[0][0] > 0.5  # Returns True if "Real", False if "Fake"

# Function to interact with the contract to create a product
def add_product_to_blockchain(price, image_hash):
    seller_address = w3.eth.accounts[0]  # Replace with user wallet address if using MetaMask
    tx = contract.functions.setProduct(price, image_hash).transact({"from": seller_address, "gas": 500000})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt

# Function to purchase the product automatically
def purchase_product(product_id, price):
    buyer_address = w3.eth.accounts[1]  # Replace with a dynamic account for the buyer
    tx = contract.functions.buyProduct(product_id).transact({
        "from": buyer_address,
        "value": price,
        "gas": 500000
    })
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt

# Main app logic
def main():
    st.title("🔒 Trustify: Product Verification")

    # Upload image
    uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
    
    # Enter product price
    price = st.number_input("Enter Product Price (in Wei)", min_value=1, step=1)

    # Submit button
    if st.button("Submit Product"):
        if uploaded_file and price:
            # Generate image hash
            image_hash = generate_image_hash(uploaded_file)
            st.write(f"Generated Image Hash: {image_hash}")

            # Perform AI verification
            is_real = predict_image(uploaded_file)
            if is_real:
                st.success("✅ Product Verified as Real. Proceeding to purchase...")

                # Add product to the blockchain
                try:
                    receipt = add_product_to_blockchain(price, image_hash)
                    st.write(f"Product added successfully! Transaction Hash: {receipt['transactionHash'].hex()}")

                    # # Print the entire receipt for debugging
                    # st.write("Transaction Receipt:", receipt)

                    logs = receipt["logs"]

                    if logs:
                        try:
                            # Decode the event logs using the contract's event ABI
                            product_created_event = contract.events.ProductCreated()
                            event_data = product_created_event.process_receipt(receipt)
                            
                            if event_data:
                                # The first event in the receipt
                                product_id = event_data[0]['args']['productId']
                                st.write(f"Product ID: {product_id}")

                                # Automatically purchase the product
                                try:
                                    purchase_receipt = purchase_product(product_id, price)
                                    st.success(f"Product purchased successfully! Transaction Hash: {purchase_receipt['transactionHash'].hex()}")
                                except Exception as e:
                                    st.error(f"Error purchasing product: {e}")
                            else:
                                st.error("No ProductCreated event found in the receipt.")
                        except Exception as e:
                            st.error(f"Error processing event logs: {e}")
                except Exception as e:
                    st.error(f"Error adding product to blockchain: {e}")

                # Print the entire receipt for debugging
                st.write("Transaction Receipt:", receipt)
            else:
                st.error("❌ Product Verification Failed: The product is classified as Fake.")
        else:
            st.error("Please upload an image and enter a valid price.")


if __name__ == "__main__":
    main()
