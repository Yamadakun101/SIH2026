from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from mock_official_system.keys import get_provider_private_key, get_provider_public_key

def sign_data_hash(data_hash: str) -> str:
    """Signs a SHA-256 digest string using the official provider's private Ed25519 key."""
    private_key = get_provider_private_key()
    signature_bytes = private_key.sign(data_hash.encode("utf-8"))
    return signature_bytes.hex()

def verify_data_signature(data_hash: str, signature_hex: str, public_key_hex: str) -> bool:
    """Verifies an Ed25519 signature over a SHA-256 digest string."""
    try:
        public_bytes = bytes.fromhex(public_key_hex)
        sig_bytes = bytes.fromhex(signature_hex)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
        public_key.verify(sig_bytes, data_hash.encode("utf-8"))
        return True
    except (InvalidSignature, ValueError, Exception):
        return False
