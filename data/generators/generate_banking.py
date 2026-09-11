import csv
import json
from datetime import datetime
from data.generators.generators_common import (
    BANKING_DIR, MULE_ACCOUNT, MULE_VPA, ATM_CIVIL_LINES
)
from backend.app.ingestion.envelope import create_envelope

def generate_banking():
    txs = [
        {
            "tx_id": "BANK-TX-4401",
            "timestamp": "2026-09-02T22:05:00Z",
            "account_number": MULE_ACCOUNT,
            "upi_vpa": MULE_VPA,
            "tx_type": "ATM_CASH_WITHDRAWAL",
            "amount_inr": 45000.0,
            "balance_after_inr": 1250.0,
            "terminal_id": ATM_CIVIL_LINES,
            "channel": "ATM",
            "remarks": "Rapid Cash Dispense Civil Lines Delhi"
        },
        {
            "tx_id": "BANK-TX-4398",
            "timestamp": "2026-09-02T21:50:00Z",
            "account_number": MULE_ACCOUNT,
            "upi_vpa": MULE_VPA,
            "tx_type": "UPI_CREDIT",
            "amount_inr": 25000.0,
            "balance_after_inr": 46250.0,
            "terminal_id": "UPI-GATEWAY-IN",
            "channel": "UPI",
            "remarks": "P2P transfer from anonymous wallet ID 9871044219@paytm"
        },
        {
            "tx_id": "BANK-TX-4395",
            "timestamp": "2026-09-02T21:35:00Z",
            "account_number": MULE_ACCOUNT,
            "upi_vpa": MULE_VPA,
            "tx_type": "UPI_CREDIT",
            "amount_inr": 20000.0,
            "balance_after_inr": 21250.0,
            "terminal_id": "UPI-GATEWAY-IN",
            "channel": "UPI",
            "remarks": "IMPS transfer from Travel Agency shell account"
        },
        {
            "tx_id": "BANK-TX-4410",
            "timestamp": "2026-09-02T22:45:00Z",
            "account_number": MULE_ACCOUNT,
            "upi_vpa": MULE_VPA,
            "tx_type": "NEFT_TRANSFER_OUT",
            "amount_inr": 150000.0,
            "balance_after_inr": 3200.0,
            "terminal_id": "NETBANKING-IP-103.41",
            "channel": "NEFT",
            "remarks": "Logistics clearing transit payment to Panipat Lodge Account"
        }
    ]

    # Save as CSV
    csv_path = BANKING_DIR / "bank_statements.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=txs[0].keys())
        writer.writeheader()
        writer.writerows(txs)

    # Wrap in canonical envelopes and save JSON
    envelopes = []
    for record in txs:
        env = create_envelope(
            source_type="BANK",
            raw_content=record,
            badge_id="DL-INV-301",
            record_id=f"REC-{record['tx_id']}"
        )
        envelopes.append(env)

    json_path = BANKING_DIR / "banking_envelopes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(envelopes, f, indent=2)

    print(f"[+] Generated {len(txs)} Banking records in {BANKING_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_banking()
