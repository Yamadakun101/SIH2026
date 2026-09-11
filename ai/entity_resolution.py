"""
Entity Resolution & Disambiguation Engine
Resolves multi-source fragmented entity mentions into unified canonical node entities.
"""

import re
from typing import Any, Dict, List, Optional
from .ner_extractor import ExtractedEntity


class ResolvedEntityLink:
    """Represents a resolved link between an extracted raw entity and a canonical graph node."""

    def __init__(
        self,
        canonical_node_id: str,
        canonical_label: str,
        node_type: str,
        confidence: float,
        resolution_rule: str,
        raw_mentions: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.canonical_node_id = canonical_node_id
        self.canonical_label = canonical_label
        self.node_type = node_type
        self.confidence = confidence
        self.resolution_rule = resolution_rule
        self.raw_mentions = raw_mentions
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "canonical_node_id": self.canonical_node_id,
            "canonical_label": self.canonical_label,
            "node_type": self.node_type,
            "confidence": round(self.confidence, 3),
            "resolution_rule": self.resolution_rule,
            "mention_count": len(self.raw_mentions),
            "raw_mentions": self.raw_mentions,
            "metadata": self.metadata,
        }


class EntityResolver:
    """Disambiguates and links extracted entities to canonical network graph nodes."""

    # Canonical node mapping table for case DL-2026-0412
    CANONICAL_TARGETS = [
        {
            "node_id": "person-priya",
            "label": "Priya Sharma",
            "type": "PERSON",
            "aliases": ["priya", "priya sharma", "victim", "complainant's daughter"],
        },
        {
            "node_id": "person-rakesh",
            "label": "Rakesh Kumar",
            "type": "PERSON",
            "aliases": ["rakesh", "rakesh kumar", "raka", "rk", "r.k."],
        },
        {
            "node_id": "person-vikram",
            "label": "Vikram Singh",
            "type": "PERSON",
            "aliases": ["vikram", "vikram singh", "vicky"],
        },
        {
            "node_id": "phone-priya",
            "label": "+91 98112 00341",
            "type": "PHONE",
            "aliases": ["9811200341", "+919811200341", "98112 00341"],
        },
        {
            "node_id": "phone-burner-rakesh",
            "label": "+91 98710 44219",
            "type": "PHONE",
            "aliases": ["9871044219", "+919871044219", "98710 44219", "burner sim"],
        },
        {
            "node_id": "phone-vikram",
            "label": "+91 97115 88201",
            "type": "PHONE",
            "aliases": ["9711588201", "+919711588201", "97115 88201"],
        },
        {
            "node_id": "vehicle-dl01-9921",
            "label": "DL 01 AB 9921",
            "type": "VEHICLE",
            "aliases": ["dl01ab9921", "dl 01 ab 9921", "dl 01 ab9921", "white swift dzire", "dl-01-ab-9921"],
        },
        {
            "node_id": "loc-kashmere-gate",
            "label": "ISBT Kashmere Gate",
            "type": "LOCATION",
            "aliases": ["isbt kashmere gate", "kashmere gate", "isbt"],
        },
        {
            "node_id": "loc-singhu-border",
            "label": "Singhu Border Toll Plaza",
            "type": "LOCATION",
            "aliases": ["singhu border", "singhu toll", "singhu border toll plaza", "singhu"],
        },
        {
            "node_id": "bank-mule-01",
            "label": "HDFC A/C ••4091",
            "type": "BANK_ACCOUNT",
            "aliases": ["4091", "hdfc ••4091", "rkenterprises@okhdfc", "rk enterprises"],
        },
    ]

    @staticmethod
    def normalize_phone(raw_phone: str) -> str:
        """Strip formatting and normalize to 10-digit number."""
        digits = re.sub(r"\D", "", raw_phone)
        if len(digits) == 12 and digits.startswith("91"):
            return digits[2:]
        return digits

    @staticmethod
    def normalize_vehicle(raw_plate: str) -> str:
        """Strip spaces and dashes from vehicle plate."""
        return re.sub(r"[^A-Za-z0-9]", "", raw_plate).upper()

    def resolve_entity(self, entity: ExtractedEntity) -> Optional[ResolvedEntityLink]:
        """Resolve a single extracted entity mention to its canonical node."""
        raw_lower = entity.raw_text.lower().strip()
        norm_val = entity.normalized_value

        # Match by phone digits
        if entity.entity_type == "PHONE":
            extracted_digits = self.normalize_phone(norm_val)
            for target in self.CANONICAL_TARGETS:
                if target["type"] == "PHONE":
                    for alias in target["aliases"]:
                        if self.normalize_phone(alias) == extracted_digits:
                            return ResolvedEntityLink(
                                canonical_node_id=target["node_id"],
                                canonical_label=target["label"],
                                node_type="PHONE",
                                confidence=0.98,
                                resolution_rule="EXACT_PHONE_DIGITS_MATCH",
                                raw_mentions=[entity.to_dict()],
                            )

        # Match by vehicle registration
        if entity.entity_type == "VEHICLE":
            extracted_norm = self.normalize_vehicle(norm_val)
            for target in self.CANONICAL_TARGETS:
                if target["type"] == "VEHICLE":
                    for alias in target["aliases"]:
                        if self.normalize_vehicle(alias) == extracted_norm:
                            return ResolvedEntityLink(
                                canonical_node_id=target["node_id"],
                                canonical_label=target["label"],
                                node_type="VEHICLE",
                                confidence=0.97,
                                resolution_rule="EXACT_VEHICLE_PLATE_NORM",
                                raw_mentions=[entity.to_dict()],
                            )

        # Match by person aliases or bank / location
        for target in self.CANONICAL_TARGETS:
            if target["type"] == entity.entity_type or (
                entity.entity_type in ["BANK_ACCOUNT", "UPI_VPA"] and target["type"] == "BANK_ACCOUNT"
            ):
                for alias in target["aliases"]:
                    if alias in raw_lower or raw_lower in alias or alias in norm_val.lower():
                        return ResolvedEntityLink(
                            canonical_node_id=target["node_id"],
                            canonical_label=target["label"],
                            node_type=target["type"],
                            confidence=0.92,
                            resolution_rule="ALIAS_DICTIONARY_MATCH",
                            raw_mentions=[entity.to_dict()],
                        )

        return None

    def resolve_batch(self, entities: List[ExtractedEntity]) -> List[ResolvedEntityLink]:
        """Resolve multiple entity mentions, grouping mentions of the same canonical entity."""
        grouped: Dict[str, ResolvedEntityLink] = {}

        for ent in entities:
            resolved = self.resolve_entity(ent)
            if not resolved:
                continue

            nid = resolved.canonical_node_id
            if nid in grouped:
                grouped[nid].raw_mentions.extend(resolved.raw_mentions)
                # Boost confidence slightly when supported by multiple source mentions
                grouped[nid].confidence = min(0.99, grouped[nid].confidence + 0.02)
            else:
                grouped[nid] = resolved

        return list(grouped.values())
