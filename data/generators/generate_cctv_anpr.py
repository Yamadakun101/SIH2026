import csv
import json
from data.generators.generators_common import (
    CCTV_DIR, VIKRAM_VEHICLE, ANPR_SINGHU
)
from backend.app.ingestion.envelope import create_envelope

def generate_cctv_anpr():
    sightings = [
        {
            "log_id": "CCTV-KASHMERE-01",
            "timestamp": "2026-09-02T21:35:10Z",
            "camera_id": "CAM-ISBT-GATE-2",
            "location_name": "ISBT Kashmere Gate Exit Ring Road",
            "license_plate": VIKRAM_VEHICLE,
            "vehicle_type": "SEDAN_WHITE",
            "speed_kmph": 28.5,
            "lane_number": 1,
            "confidence_pct": 98.4,
            "image_frame_hash": "e8a910bf23c4a5b6c7d8e9f0123456789abcdef0123456789abcdef012345678"
        },
        {
            "log_id": "CCTV-MAJNU-04",
            "timestamp": "2026-09-02T21:55:40Z",
            "camera_id": "ANPR-MAJNU-FLYOVER-N",
            "location_name": "Outer Ring Road Majnu Ka Tilla Northbound",
            "license_plate": VIKRAM_VEHICLE,
            "vehicle_type": "SEDAN_WHITE",
            "speed_kmph": 64.2,
            "lane_number": 2,
            "confidence_pct": 99.1,
            "image_frame_hash": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0"
        },
        {
            "log_id": "ANPR-TOLL-SINGHU-04",
            "timestamp": "2026-09-02T22:15:00Z",
            "camera_id": ANPR_SINGHU,
            "location_name": "Singhu Border Toll Plaza Haryana Exit",
            "license_plate": VIKRAM_VEHICLE,
            "vehicle_type": "SEDAN_WHITE",
            "speed_kmph": 78.0,
            "lane_number": 4,
            "confidence_pct": 99.8,
            "image_frame_hash": "7b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c"
        }
    ]

    # Save as CSV
    csv_path = CCTV_DIR / "anpr_toll_sightings.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sightings[0].keys())
        writer.writeheader()
        writer.writerows(sightings)

    # Wrap in canonical envelopes and save JSON
    envelopes = []
    for record in sightings:
        env = create_envelope(
            source_type="CCTV_ANPR",
            raw_content=record,
            badge_id="DP-HW-881",
            record_id=f"REC-{record['log_id']}"
        )
        envelopes.append(env)

    json_path = CCTV_DIR / "cctv_anpr_envelopes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(envelopes, f, indent=2)

    print(f"[+] Generated {len(sightings)} CCTV/ANPR records in {CCTV_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_cctv_anpr()
