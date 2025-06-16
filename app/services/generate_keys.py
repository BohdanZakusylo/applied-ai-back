from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# Define the paths
PRIVATE_KEY_PATH = "app/keys/private_key.pem"
PUBLIC_KEY_PATH = "app/keys/public_key.pem"

def generate_rsa_keys():
    # Make sure the directory exists
    os.makedirs(os.path.dirname(PRIVATE_KEY_PATH), exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write to files
    with open(PRIVATE_KEY_PATH, 'wb') as f:
        f.write(private_pem)
    
    with open(PUBLIC_KEY_PATH, 'wb') as f:
        f.write(public_pem)
    
    print(f"Keys generated successfully:")
    print(f"Private key saved to: {os.path.abspath(PRIVATE_KEY_PATH)}")
    print(f"Public key saved to: {os.path.abspath(PUBLIC_KEY_PATH)}")

if __name__ == "__main__":
    generate_rsa_keys()
