from typing import Set

class ReplayProtectionTracker:
    """Tracks consumed nonces and request IDs to prevent replay attacks."""
    def __init__(self):
        self._consumed_nonces: Set[str] = set()
        self._processed_requests: Set[str] = set()

    def is_replayed(self, request_id: str, nonce: str) -> bool:
        if nonce in self._consumed_nonces:
            return True
        if request_id in self._processed_requests:
            return True
        return False

    def mark_consumed(self, request_id: str, nonce: str):
        self._consumed_nonces.add(nonce)
        self._processed_requests.add(request_id)

    def reset(self):
        self._consumed_nonces.clear()
        self._processed_requests.clear()

replay_tracker = ReplayProtectionTracker()
