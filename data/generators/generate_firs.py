import json
from data.generators.generators_common import FIRS_DIR, CASE_ID
from backend.app.ingestion.envelope import create_envelope

def generate_firs():
    firs = [
        {
            "fir_number": "FIR-412/2026/PS-KashmereGate",
            "case_id": CASE_ID,
            "police_station": "PS Kashmere Gate, North District, Delhi",
            "date_of_registration": "2026-09-03T08:30:00Z",
            "date_of_occurrence": "2026-09-02T22:00:00Z",
            "acts_sections": ["BNS Section 137(2) (Kidnapping)", "BNS Section 143 (Human Trafficking)"],
            "complainant_name": "Rajesh Sharma",
            "complainant_relation": "Father",
            "victim_name": "Priya Sharma",
            "victim_age": 22,
            "incident_narrative": "Complainant reports that his daughter Priya did not return from college in North Campus. Her mobile phone (+91 98112 00341) was found active near ISBT Kashmere Gate around 21:45 hrs on 02-Sep-2026 before being abruptly powered off.",
            "investigating_officer": "Sub-Inspector Deepak Rawat",
            "io_badge_number": "DP-SI-4921",
            "status": "UNDER_ACTIVE_INVESTIGATION"
        },
        {
            "fir_number": "FIR-418/2026/PS-MajnuKaTilla",
            "case_id": "DL-2026-0418",
            "police_station": "PS Majnu Ka Tilla, Delhi",
            "date_of_registration": "2026-09-01T14:15:00Z",
            "date_of_occurrence": "2026-09-01T11:00:00Z",
            "acts_sections": ["BNS Section 318 (Cheating)", "BNS Section 336 (Forged Documents)"],
            "complainant_name": "Sunil Verma",
            "complainant_relation": "Store Owner",
            "victim_name": "Telecom Franchise",
            "victim_age": None,
            "incident_narrative": "Unauthorized bulk SIM activation using forged Aadhaar photocopies reported at franchise counter. Handset IMEI footprints linked to syndicate operator known alias Raka.",
            "investigating_officer": "Inspector Manoj Kumar",
            "io_badge_number": "DP-INSP-1092",
            "status": "LINKED_INVESTIGATION"
        }
    ]

    envelopes = []
    for fir in firs:
        rec_id = f"REC-FIR-{fir['fir_number'].split('/')[0]}"
        env = create_envelope(
            source_type="FIR",
            raw_content=fir,
            badge_id=fir.get("io_badge_number", "DP-SI-4921"),
            record_id=rec_id
        )
        envelopes.append(env)
        
        # Save individual file
        file_path = FIRS_DIR / f"{fir['fir_number'].replace('/', '_')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(env, f, indent=2)

    print(f"[+] Generated {len(envelopes)} FIR records in {FIRS_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_firs()
