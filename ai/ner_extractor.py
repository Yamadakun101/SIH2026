"""
Multi-Source Named Entity Recognition (NER) Extractor
Extracts structured entities (Phones, Vehicles, Bank Accounts, UPI VPAs, Names, Locations) from raw text.
"""

import re
from typing import Any, Dict, List, Optional


class ExtractedEntity:
    """Represents an entity extracted from raw investigative text."""

    def __init__(
        self,
        entity_type: str,
        raw_text: str,
        normalized_value: str,
        start_char: int,
        end_char: int,
        confidence: float,
        source_context: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.entity_type = entity_type.upper()
        self.raw_text = raw_text
        self.normalized_value = normalized_value
        self.start_char = start_char
        self.end_char = end_char
        self.confidence = confidence
        self.source_context = source_context
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "raw_text": self.raw_text,
            "normalized_value": self.normalized_value,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "confidence": round(self.confidence, 3),
            "source_context": self.source_context,
            "metadata": self.metadata,
        }


class MultiSourceNERExtractor:
    """Extracts entities from raw crime documents using domain-specific heuristics and patterns."""

    # Indian Vehicle Registration Number regex: e.g. DL 01 AB 9921, HR 26 DQ 8812, DL-14201900381
    VEHICLE_REGEX = re.compile(
        r"\b([A-Z]{2}[-\s]?[0-9]{1,2}[-\s]?[A-Z]{1,3}[-\s]?[0-9]{4})\b",
        re.IGNORECASE
    )

    # Indian Phone regex: e.g. +91 98710 44219, +91-98112-00341, 9871044219
    PHONE_REGEX = re.compile(
        r"(?:\+91[\s-]?)?([6-9]\d{4}[\s-]?\d{5})\b"
    )

    # UPI VPA regex: e.g. rkenterprises@okhdfc, user123@paytm, 9871044219@ybl
    UPI_REGEX = re.compile(
        r"\b([a-zA-Z0-9.\-_]{2,256}@(okhdfc|okaxis|oksbi|paytm|ybl|apl|axl|ibl))\b",
        re.IGNORECASE
    )

    # Bank Account mention regex: e.g. HDFC A/C ••4091, A/C 50100293819201, IFSC HDFC0001204
    BANK_ACC_REGEX = re.compile(
        r"\b(?:A/C|Account|Acct|A/c)[:\s]*([0-9Xx•]{4,18})\b",
        re.IGNORECASE
    )
    IFSC_REGEX = re.compile(
        r"\b([A-Z]{4}0[A-Z0-9]{6})\b",
        re.IGNORECASE
    )

    # Fastag ID regex: e.g. FASTAG-TX-8812
    FASTAG_REGEX = re.compile(
        r"\b(FASTAG-[A-Z0-9-]+)\b",
        re.IGNORECASE
    )

    # Cell Tower / ANPR device ID regex
    TOWER_ANPR_REGEX = re.compile(
        r"\b(TOW-[A-Z0-9-]+|ANPR-[A-Z0-9-]+|CDR-[A-Z0-9-]+)\b",
        re.IGNORECASE
    )

    # Known locations in Delhi / interstate transit context
    KNOWN_LOCATIONS = [
        "ISBT Kashmere Gate",
        "Kashmere Gate",
        "Majnu Ka Tilla",
        "Singhu Border",
        "Singhu Border Toll Plaza",
        "Civil Lines",
        "Laxmi Nagar",
        "Ambala",
        "Ambala Transit Point",
        "Chandigarh",
        "Rohini",
        "Connaught Place",
    ]

    # Known fictional demo person names and aliases
    KNOWN_PERSONS = {
        "priya sharma": "Priya Sharma",
        "priya": "Priya Sharma",
        "rakesh kumar": "Rakesh Kumar",
        "rakesh": "Rakesh Kumar",
        "raka": "Rakesh Kumar",
        "rk": "Rakesh Kumar",
        "vikram singh": "Vikram Singh",
        "vikram": "Vikram Singh",
        "vicky": "Vikram Singh",
    }

    def extract_all(self, text: str, source_context: str = "") -> List[ExtractedEntity]:
        """Extract all typed entities found within raw text."""
        entities: List[ExtractedEntity] = []

        # 1. Extract Phone Numbers
        for m in self.PHONE_REGEX.finditer(text):
            raw = m.group(0)
            digits = re.sub(r"\D", "", raw)
            if len(digits) == 10:
                norm_phone = f"+91 {digits[:5]} {digits[5:]}"
            elif len(digits) == 12 and digits.startswith("91"):
                norm_phone = f"+91 {digits[2:7]} {digits[7:]}"
            else:
                norm_phone = raw

            entities.append(ExtractedEntity(
                entity_type="PHONE",
                raw_text=raw,
                normalized_value=norm_phone,
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.96,
                source_context=source_context,
            ))

        # 2. Extract Vehicles
        for m in self.VEHICLE_REGEX.finditer(text):
            raw = m.group(0)
            cleaned = re.sub(r"[-\s]", " ", raw).upper()
            entities.append(ExtractedEntity(
                entity_type="VEHICLE",
                raw_text=raw,
                normalized_value=cleaned,
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.95,
                source_context=source_context,
            ))

        # 3. Extract UPI VPAs
        for m in self.UPI_REGEX.finditer(text):
            raw = m.group(1)
            entities.append(ExtractedEntity(
                entity_type="BANK_ACCOUNT",
                raw_text=raw,
                normalized_value=raw.lower(),
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.98,
                source_context=source_context,
                metadata={"subtype": "UPI_VPA"},
            ))

        # 4. Extract Bank Accounts & IFSC
        for m in self.BANK_ACC_REGEX.finditer(text):
            raw = m.group(1)
            entities.append(ExtractedEntity(
                entity_type="BANK_ACCOUNT",
                raw_text=raw,
                normalized_value=f"A/C ••{raw[-4:]}" if len(raw) >= 4 else raw,
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.92,
                source_context=source_context,
                metadata={"subtype": "BANK_ACCOUNT_NUM"},
            ))

        # 5. Extract Fastags & Device IDs
        for m in self.FASTAG_REGEX.finditer(text):
            raw = m.group(1)
            entities.append(ExtractedEntity(
                entity_type="DEVICE",
                raw_text=raw,
                normalized_value=raw.upper(),
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.97,
                source_context=source_context,
                metadata={"subtype": "FASTAG"},
            ))

        for m in self.TOWER_ANPR_REGEX.finditer(text):
            raw = m.group(1)
            entities.append(ExtractedEntity(
                entity_type="SURVEILLANCE_NODE",
                raw_text=raw,
                normalized_value=raw.upper(),
                start_char=m.start(),
                end_char=m.end(),
                confidence=0.99,
                source_context=source_context,
            ))

        # 6. Extract Known Locations
        lower_text = text.lower()
        for loc in self.KNOWN_LOCATIONS:
            idx = 0
            while True:
                found_idx = lower_text.find(loc.lower(), idx)
                if found_idx == -1:
                    break
                raw = text[found_idx: found_idx + len(loc)]
                entities.append(ExtractedEntity(
                    entity_type="LOCATION",
                    raw_text=raw,
                    normalized_value=loc,
                    start_char=found_idx,
                    end_char=found_idx + len(loc),
                    confidence=0.94,
                    source_context=source_context,
                ))
                idx = found_idx + len(loc)

        # 7. Extract Known Person Names & Aliases
        for alias_key, canon_name in self.KNOWN_PERSONS.items():
            pattern = rf"\b{re.escape(alias_key)}\b"
            for m in re.finditer(pattern, text, re.IGNORECASE):
                raw = m.group(0)
                entities.append(ExtractedEntity(
                    entity_type="PERSON",
                    raw_text=raw,
                    normalized_value=canon_name,
                    start_char=m.start(),
                    end_char=m.end(),
                    confidence=0.93 if raw.lower() == canon_name.lower() else 0.88,
                    source_context=source_context,
                    metadata={"alias_matched": raw, "canonical": canon_name},
                ))

        # Deduplicate identical entity spans
        unique_entities: List[ExtractedEntity] = []
        seen_spans = set()
        for ent in entities:
            span_key = (ent.entity_type, ent.start_char, ent.end_char)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                unique_entities.append(ent)

        return sorted(unique_entities, key=lambda x: x.start_char)
