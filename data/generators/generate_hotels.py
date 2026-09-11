import csv
import json
from data.generators.generators_common import (
    HOTELS_DIR, RAKESH_PHONE, VIKRAM_PHONE
)
from backend.app.ingestion.envelope import create_envelope

def generate_hotels():
    records = [
        {
            "register_id": "HTL-DEL-MAJNU-81",
            "lodge_name": "Riverside Comfort Inn, Majnu Ka Tilla",
            "check_in_time": "2026-09-02T14:30:00Z",
            "check_out_time": "2026-09-02T20:45:00Z",
            "guest_name_entered": "R. Kumar",
            "id_proof_type": "AADHAAR_PHOTOCOPY",
            "id_proof_number_masked": "•••• •••• 9921",
            "contact_number": RAKESH_PHONE,
            "room_number": "304",
            "accompanying_person": "Vikram S.",
            "payment_mode": "CASH"
        },
        {
            "register_id": "HTL-HR-AMBALA-12",
            "lodge_name": "Highway Tourist Rest House, Ambala GT Road",
            "check_in_time": "2026-09-03T01:15:00Z",
            "check_out_time": "2026-09-03T05:30:00Z",
            "guest_name_entered": "Vicky Singh",
            "id_proof_type": "DRIVING_LICENSE",
            "id_proof_number_masked": "DL-••••••••381",
            "contact_number": VIKRAM_PHONE,
            "room_number": "108",
            "accompanying_person": "2 Guests Unregistered",
            "payment_mode": "UPI"
        }
    ]

    # Save as CSV
    csv_path = HOTELS_DIR / "hotel_lodge_registers.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    # Wrap in canonical envelopes and save JSON
    envelopes = []
    for record in records:
        env = create_envelope(
            source_type="HOTEL",
            raw_content=record,
            badge_id="DL-INV-301",
            record_id=f"REC-{record['register_id']}"
        )
        envelopes.append(env)

    json_path = HOTELS_DIR / "hotel_envelopes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(envelopes, f, indent=2)

    print(f"[+] Generated {len(records)} Hotel/Lodge records in {HOTELS_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_hotels()
