import re
from datetime import datetime, timezone
from typing import Optional

def normalize_phone(phone: str) -> str:
    """Normalizes phone numbers to standard Indian E.164 format (+91XXXXXXXXXX)."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("91") and len(digits) == 12:
        return f"+{digits}"
    elif digits.startswith("0") and len(digits) == 11:
        return f"+91{digits[1:]}"
    elif len(digits) == 10:
        return f"+91{digits}"
    return phone.strip()

def normalize_license_plate(plate: str) -> str:
    """Normalizes Indian vehicle license plates to standard format (e.g. DL 01 AB 9921)."""
    clean = re.sub(r"[^A-Za-z0-9]", "", plate).upper()
    # Match pattern: 2 letters (State), 2 digits (RTO), 1-3 letters (Series), 4 digits (Number)
    match = re.match(r"^([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{1,4})$", clean)
    if match:
        state, rto, series, num = match.groups()
        return f"{state} {int(rto):02d} {series} {int(num):04d}"
    return plate.strip().upper()

def normalize_timestamp(ts_str: str) -> str:
    """Normalizes timestamps to standard ISO 8601 UTC string."""
    try:
        if ts_str.endswith("Z"):
            ts_str = ts_str[:-1] + "+00:00"
        dt = datetime.fromisoformat(ts_str)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ts_str.strip()

def normalize_upi_vpa(vpa: str) -> str:
    """Normalizes UPI Virtual Payment Address (lowercase, trimmed)."""
    return vpa.strip().lower()
