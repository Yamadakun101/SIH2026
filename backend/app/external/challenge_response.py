from mock_official_system.authentication import build_canonical_message, compute_hmac

def generate_client_hmac_proof(
    client_id: str,
    request_id: str,
    nonce: str,
    timestamp: str,
    resource: str,
    shared_secret: str
) -> str:
    """Computes HMAC-SHA-256 challenge proof using the shared secret."""
    canonical_message = build_canonical_message(client_id, request_id, nonce, timestamp, resource)
    return compute_hmac(shared_secret, canonical_message)
