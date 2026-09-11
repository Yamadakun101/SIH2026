"""
SHA-256 Merkle Hash-Chain & Tamper-Evident Evidence Ledger
Provides cryptographic chain-of-custody tracking for multi-source crime data.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def canonical_json_bytes(data: Any) -> bytes:
    """Serialize data into deterministic canonical JSON bytes."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """Compute SHA-256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


class MerkleTree:
    """Binary Merkle Tree implementation with inclusion proofs."""

    def __init__(self, leaf_hashes: Optional[List[str]] = None):
        self.leaves: List[str] = leaf_hashes or []
        self.tree_levels: List[List[str]] = []
        self._build_tree()

    def _build_tree(self) -> None:
        if not self.leaves:
            self.root: str = sha256_hex(b"")
            self.tree_levels = [[]]
            return

        current_level = list(self.leaves)
        self.tree_levels = [current_level]

        while len(current_level) > 1:
            next_level: List[str] = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left  # Duplicate last element if odd

                combined = (left + right).encode("utf-8")
                parent_hash = sha256_hex(combined)
                next_level.append(parent_hash)

            current_level = next_level
            self.tree_levels.append(current_level)

        self.root = self.tree_levels[-1][0]

    def get_merkle_root(self) -> str:
        return self.root

    def get_inclusion_proof(self, leaf_index: int) -> List[Dict[str, str]]:
        """Generate audit path for a specific leaf index."""
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise IndexError("Leaf index out of bounds.")

        proof: List[Dict[str, str]] = []
        idx = leaf_index

        for level in self.tree_levels[:-1]:
            is_right_sibling = (idx % 2 == 0)
            sibling_idx = idx + 1 if is_right_sibling else idx - 1

            if sibling_idx < len(level):
                sibling_hash = level[sibling_idx]
            else:
                sibling_hash = level[idx]  # Self duplicated

            proof.append({
                "position": "right" if is_right_sibling else "left",
                "hash": sibling_hash
            })
            idx = idx // 2

        return proof

    @staticmethod
    def verify_proof(leaf_hash: str, proof: List[Dict[str, str]], expected_root: str) -> bool:
        """Verify inclusion of a leaf hash against a root."""
        current = leaf_hash
        for step in proof:
            sibling = step["hash"]
            if step["position"] == "right":
                combined = (current + sibling).encode("utf-8")
            else:
                combined = (sibling + current).encode("utf-8")
            current = sha256_hex(combined)
        return current == expected_root


class EvidenceBlock:
    """Represents a single tamper-evident record block in the custody chain."""

    def __init__(
        self,
        block_index: int,
        record_id: str,
        source_type: str,
        timestamp: str,
        officer_badge: str,
        action: str,
        data_payload: Dict[str, Any],
        prev_block_hash: str,
        data_hash: Optional[str] = None,
        block_hash: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.block_index = block_index
        self.record_id = record_id
        self.source_type = source_type
        self.timestamp = timestamp
        self.officer_badge = officer_badge
        self.action = action
        self.data_payload = data_payload
        self.prev_block_hash = prev_block_hash
        self.metadata = metadata or {}

        # Compute data hash if not provided
        self.data_hash = data_hash or self.calculate_data_hash()
        # Compute block hash if not provided
        self.block_hash = block_hash or self.calculate_block_hash()

    def calculate_data_hash(self) -> str:
        return sha256_hex(canonical_json_bytes(self.data_payload))

    def calculate_block_hash(self) -> str:
        header_data = {
            "block_index": self.block_index,
            "record_id": self.record_id,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "officer_badge": self.officer_badge,
            "action": self.action,
            "data_hash": self.data_hash,
            "prev_block_hash": self.prev_block_hash,
        }
        return sha256_hex(canonical_json_bytes(header_data))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_index": self.block_index,
            "record_id": self.record_id,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "officer_badge": self.officer_badge,
            "action": self.action,
            "data_payload": self.data_payload,
            "data_hash": self.data_hash,
            "prev_block_hash": self.prev_block_hash,
            "block_hash": self.block_hash,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvidenceBlock":
        return cls(
            block_index=data["block_index"],
            record_id=data["record_id"],
            source_type=data["source_type"],
            timestamp=data["timestamp"],
            officer_badge=data["officer_badge"],
            action=data["action"],
            data_payload=data["data_payload"],
            prev_block_hash=data["prev_block_hash"],
            data_hash=data.get("data_hash"),
            block_hash=data.get("block_hash"),
            metadata=data.get("metadata", {}),
        )


class EvidenceHashChain:
    """Cryptographic chain-of-custody log with Merkle tree integrity verification."""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.blocks: List[EvidenceBlock] = []

    def create_genesis_block(
        self,
        officer_badge: str = "SYSTEM_INITIALIZER",
        timestamp: Optional[str] = None,
        notes: str = "Case Evidence Custody Chain Initialized"
    ) -> EvidenceBlock:
        """Create and append the immutable genesis block."""
        if self.blocks:
            raise ValueError("Genesis block already created for this case chain.")

        ts = timestamp or datetime.now(timezone.utc).isoformat()
        genesis_payload = {
            "case_id": self.case_id,
            "initialization_notice": notes,
            "standard": "BSA_2023_SECTION_63_COMPLIANT",
        }
        genesis_block = EvidenceBlock(
            block_index=0,
            record_id=f"GENESIS-{self.case_id}",
            source_type="SYSTEM_GENESIS",
            timestamp=ts,
            officer_badge=officer_badge,
            action="CHAIN_INITIALIZATION",
            data_payload=genesis_payload,
            prev_block_hash="0" * 64,
        )
        self.blocks.append(genesis_block)
        return genesis_block

    def append_evidence(
        self,
        record_id: str,
        source_type: str,
        data_payload: Dict[str, Any],
        officer_badge: str,
        action: str = "INGESTED",
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvidenceBlock:
        """Add a new evidence record block to the chain."""
        if not self.blocks:
            self.create_genesis_block(officer_badge=officer_badge)

        prev_hash = self.blocks[-1].block_hash
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        new_index = len(self.blocks)

        block = EvidenceBlock(
            block_index=new_index,
            record_id=record_id,
            source_type=source_type,
            timestamp=ts,
            officer_badge=officer_badge,
            action=action,
            data_payload=data_payload,
            prev_block_hash=prev_hash,
            metadata=metadata or {},
        )
        self.blocks.append(block)
        return block

    def get_merkle_root(self) -> str:
        """Calculate Merkle root of all block hashes in the chain."""
        if not self.blocks:
            return sha256_hex(b"")
        leaf_hashes = [b.block_hash for b in self.blocks]
        merkle_tree = MerkleTree(leaf_hashes)
        return merkle_tree.get_merkle_root()

    def verify_chain(self) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Validate the complete hash chain.
        Returns: (is_valid, corrupted_block_index, reason_description)
        """
        if not self.blocks:
            return True, None, "Empty chain is valid."

        # Check genesis
        genesis = self.blocks[0]
        if genesis.block_index != 0:
            return False, 0, "Genesis block index must be 0."
        if genesis.prev_block_hash != "0" * 64:
            return False, 0, "Genesis prev_block_hash must be zero-padded string."
        if genesis.calculate_data_hash() != genesis.data_hash:
            return False, 0, "Genesis data payload has been altered."
        if genesis.calculate_block_hash() != genesis.block_hash:
            return False, 0, "Genesis block header hash mismatch."

        # Check successive blocks
        for i in range(1, len(self.blocks)):
            current = self.blocks[i]
            prev = self.blocks[i - 1]

            if current.block_index != i:
                return False, i, f"Invalid block index sequence at index {i}."
            if current.prev_block_hash != prev.block_hash:
                return False, i, f"Broken link: block {i} prev_hash != block {i-1} block_hash."
            if current.calculate_data_hash() != current.data_hash:
                return False, i, f"Evidence data payload altered in block {i} (record: {current.record_id})."
            if current.calculate_block_hash() != current.block_hash:
                return False, i, f"Block hash verification failed for block {i}."

        return True, None, "All blocks and cryptographic links verified."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "total_blocks": len(self.blocks),
            "merkle_root": self.get_merkle_root(),
            "latest_block_hash": self.blocks[-1].block_hash if self.blocks else None,
            "blocks": [b.to_dict() for b in self.blocks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvidenceHashChain":
        chain = cls(case_id=data["case_id"])
        chain.blocks = [EvidenceBlock.from_dict(b) for b in data.get("blocks", [])]
        return chain
