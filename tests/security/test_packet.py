import pytest
from backend.app.external.models import SecureDataPacket
from backend.app.external.packet_verifier import verify_packet_security
from mock_official_system.packet_generator import generate_secure_packet

def test_valid_packet_verification():
    data = {"registration": "DL 01 AB 9921", "owner": "Vikram Singh", "status": "ACTIVE"}
    raw_packet = generate_secure_packet(
        request_id="REQ-TEST-PACKET-01",
        source_system="MOCK_VAHAN",
        data=data
    )
    packet = SecureDataPacket(**raw_packet)
    is_valid, reason = verify_packet_security(packet)
    assert is_valid is True
    assert "verified successfully" in reason.lower()

def test_tampered_payload_rejected():
    data = {"registration": "DL 01 AB 9921", "owner": "Vikram Singh"}
    raw_packet = generate_secure_packet(
        request_id="REQ-TEST-PACKET-02",
        source_system="MOCK_VAHAN",
        data=data
    )
    # Attacker alters data payload after signing
    raw_packet["data"]["owner"] = "TAMPERED_NAME"
    packet = SecureDataPacket(**raw_packet)

    is_valid, reason = verify_packet_security(packet)
    assert is_valid is False
    assert "integrity check failed" in reason.lower()

def test_corrupted_signature_rejected():
    data = {"registration": "DL 01 AB 9921", "owner": "Vikram Singh"}
    raw_packet = generate_secure_packet(
        request_id="REQ-TEST-PACKET-03",
        source_system="MOCK_VAHAN",
        data=data
    )
    # Corrupt the signature hex
    raw_packet["signature"]["value"] = "0" * 128
    packet = SecureDataPacket(**raw_packet)

    is_valid, reason = verify_packet_security(packet)
    assert is_valid is False
    assert "signature verification failed" in reason.lower()
