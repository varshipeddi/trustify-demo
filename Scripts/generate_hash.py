import hashlib

def generate_image_hash(image_path):
    with open(image_path, "rb") as img_file:
        return hashlib.sha256(img_file.read()).hexdigest()

# Replace with the actual image path
image_path = "C:/Users/phama/Downloads/Real Airpods-20241121T011149Z-001/Real Airpods/IMG_7553.jpg"

# Generate the hash
image_hash = generate_image_hash(image_path)
print("Image hash:", image_hash)