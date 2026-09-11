from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# Deterministic seed for repeatable mock official system testing in prototype
# (In production, keys are stored in a Hardware Security Module / KMS)
_MOCK_PRIVATE_BYTES = b"KavachNetOfficialProviderSeedKey2026!"[:32]
_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(_MOCK_PRIVATE_BYTES)
_public_key = _private_key.public_key()

def get_provider_private_key() -> ed25519.Ed25519PrivateKey:
    """Returns the official provider's private key for signing packets."""
    return _private_key

def get_provider_public_key() -> ed25519.Ed25519PublicKey:
    """Returns the official provider's public key for signature verification."""
    return _public_key

def get_provider_public_key_hex() -> str:
    """Returns public key as raw hex string."""
    raw_bytes = _public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return raw_bytes.hex()
