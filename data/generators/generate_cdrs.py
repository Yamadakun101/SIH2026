import csv
import json
from datetime import datetime, timedelta
from data.generators.generators_common import (
    CDRS_DIR, PRIYA_PHONE, PRIYA_IMEI, RAKESH_PHONE, RAKESH_IMEI,
    VIKRAM_PHONE, TOWER_KASHMERE, TOWER_SINGHU
)
from backend.app.ingestion.envelope import create_envelope

def generate_cdrs():
    base_time = datetime(2026, 9, 2, 17, 30, 0)
    cdrs = []

    # 1. 14 Calls between Rakesh and Priya between 18:00 and 21:45
    for i in range(14):
        call_time = base_time + timedelta(minutes=15 * i + 8)
        duration = 30 + (i * 12)
        if i == 13:
            # Final call at 21:45 lasting 142s
            call_time = datetime(2026, 9, 2, 21, 45, 0)
            duration = 142

        cdrs.append({
            "cdr_id": f"CDR-DEL-0902-{i+1:02d}",
            "calling_number": RAKESH_PHONE,
            "called_number": PRIYA_PHONE,
            "call_timestamp": call_time.isoformat() + "Z",
            "duration_seconds": duration,
            "call_type": "VOICE",
            "cell_tower_id": TOWER_KASHMERE,
            "calling_imei": RAKESH_IMEI,
            "called_imei": PRIYA_IMEI
        })

    # 2. 5 Coordination calls between Rakesh and Vikram
    for j in range(5):
        coord_time = datetime(2026, 9, 2, 21, 50, 0) + timedelta(minutes=10 * j)
        tower = TOWER_KASHMERE if j < 2 else TOWER_SINGHU
        cdrs.append({
            "cdr_id": f"CDR-COORD-0902-{j+1:02d}",
            "calling_number": RAKESH_PHONE,
            "called_number": VIKRAM_PHONE,
            "call_timestamp": coord_time.isoformat() + "Z",
            "duration_seconds": 45 + (j * 15),
            "call_type": "VOICE",
            "cell_tower_id": tower,
            "calling_imei": RAKESH_IMEI,
            "called_imei": "354019280192831"
        })

    # Save as CSV
    csv_path = CDRS_DIR / "cdr_triangulation_dump.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cdrs[0].keys())
        writer.writeheader()
        writer.writerows(cdrs)

    # Wrap in canonical envelopes and save JSON
    envelopes = []
    for record in cdrs:
        env = create_envelope(
            source_type="CDR",
            raw_content=record,
            badge_id="DL-INV-301",
            record_id=f"REC-{record['cdr_id']}"
        )
        envelopes.append(env)

    json_path = CDRS_DIR / "cdr_envelopes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(envelopes, f, indent=2)

    print(f"[+] Generated {len(cdrs)} CDR records (CSV + JSON) in {CDRS_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_cdrs()
