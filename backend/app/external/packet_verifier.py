from typing import Tuple
from backend.app.external.models import SecureDataPacket
from backend.app.ingestion.envelope import compute_sha256
from mock_official_system.signer import verify_data_signature

def verify_packet_security(packet: SecureDataPacket) -> Tuple[bool, str]:
    """
    Verifies the integrity and authenticity of an external SecureDataPacket:
    1. Computes SHA-256 over `data` and verifies against `integrity.hash`.
    2. Verifies the Ed25519 digital signature over the hash using `signature.public_key_hex`.
    """
    # 1. SHA-256 Data Integrity Check
    computed_hash = compute_sha256(packet.data)
    if computed_hash != packet.integrity.hash:
        return False, "Data integrity check failed: payload hash mismatch (tampered payload)"

    # 2. Digital Signature Verification
    is_sig_valid = verify_data_signature(
        data_hash=computed_hash,
        signature_hex=packet.signature.value,
        public_key_hex=packet.signature.public_key_hex
    )
    if not is_sig_valid:
        return False, "Digital signature verification failed: invalid signature"

    return True, "Packet verified successfully"
