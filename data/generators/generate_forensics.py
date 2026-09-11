import json
from data.generators.generators_common import (
    FORENSICS_DIR, CASE_ID, RAKESH_PHONE, RAKESH_IMEI, VIKRAM_PHONE, VIKRAM_VEHICLE
)
from backend.app.ingestion.envelope import create_envelope

def generate_forensics():
    reports = [
        {
            "report_id": "CYB-FSL-DEL-2026-881",
            "case_id": CASE_ID,
            "laboratory": "Cyber Forensics Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T11:00:00Z",
            "evidence_item": "Physical Device Extraction Dump — SIM Card Vi (+91 98710 44219)",
            "examiner": "Senior Scientific Officer A.K. Sharma",
            "examiner_badge": "FSL-CYB-094",
            "key_findings": {
                "hardware_imei": RAKESH_IMEI,
                "subscriber_imsi": "404450192801920",
                "activation_geofence": "Majnu Ka Tilla, Delhi",
                "deleted_chat_fragments_recovered": [
                    "Car ready at ISBT. Tell Vicky to wait near Gate 2.",
                    "Route clear through Singhu. Don't use primary phone."
                ],
                "linked_contacts": [
                    {"name": "Vicky Driver", "phone": VIKRAM_PHONE},
                    {"name": "Cash Hand", "vpa": "rkenterprises@okhdfc"}
                ],
                "cloud_backup_sync_ip": "182.74.91.22"
            },
            "investigative_implication": "Corroborates direct association between Rakesh Kumar and driver Vikram Singh."
        }
    ]

    envelopes = []
    for rep in reports:
        env = create_envelope(
            source_type="FORENSIC",
            raw_content=rep,
            badge_id=rep.get("examiner_badge", "FSL-CYB-094"),
            record_id=f"REC-{rep['report_id']}"
        )
        envelopes.append(env)

        file_path = FORENSICS_DIR / f"{rep['report_id']}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(env, f, indent=2)

    print(f"[+] Generated {len(reports)} Forensics reports in {FORENSICS_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_forensics()
