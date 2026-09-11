"""
KavachNet — Synthetic Forensic Database Expansion Generator
Generates detailed forensic records across all 8 forensic categories:
1. DNA / Biological Evidence
2. Fingerprint / Latent Print Evidence
3. Mobile / Digital Forensics (GPS, Signal artifacts, File caches)
4. CCTV / Video Forensics (Frame-by-frame analysis, gait, Re-ID)
5. Trace Evidence (Soil mineralogy, Automotive paint, Fiber)
6. Footwear / Tire Impression Evidence (Tread pitch, wear patterns)
7. Ballistics / Toolmarks (Pry marks, Stamping dies)
8. Master Chain of Custody / Evidence Integrity Ledger

All records are cryptographically sealed with SHA-256 raw envelopes
compliant with Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63.
"""

import json
from pathlib import Path
from data.generators.generators_common import (
    FORENSICS_DIR, CASE_ID, RAKESH_PHONE, RAKESH_IMEI, VIKRAM_PHONE, VIKRAM_VEHICLE
)
from backend.app.ingestion.envelope import create_envelope

def generate_forensic_expansion():
    reports = [
        # CATEGORY 1: DNA / BIOLOGICAL EVIDENCE
        {
            "report_id": "DNA-FSL-DEL-2026-401",
            "category": "DNA_BIOLOGICAL",
            "evidence_id": "EVID-DNA-001",
            "case_id": CASE_ID,
            "laboratory": "Biology Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T15:30:00Z",
            "evidence_item": "Passenger Seatbelt Buckle Swab — Vehicle DL 01 AB 9921",
            "examiner": "Senior Scientific Officer Dr. Meenakshi Sundaram",
            "examiner_badge": "FSL-BIO-042",
            "sample_id": "SMPL-BIO-DEL-401-A",
            "sample_type": "Touch DNA / Epithelial Swab",
            "biological_material": "Epithelial cellular material with nuclear DNA",
            "collection_location": "Forensic Inspection Bay, PS Kashmere Gate, Delhi",
            "collection_timestamp": "2026-09-03T11:30:00Z",
            "collection_method": "Sterile cotton swab moistened with 0.9% saline",
            "dna_profile_id": "PROF-STR-DEL-9912",
            "str_profile_metadata": {
                "kit_used": "AmpFlSTR Identifiler Plus PCR Amplification Kit",
                "loci_profile": {
                    "AMEL": ["X", "Y"],
                    "D8S1179": [13, 15],
                    "D21S11": [29, 30],
                    "D7S820": [8, 11],
                    "CSF1PO": [10, 12],
                    "D3S1358": [14, 16],
                    "TH01": [6, 9],
                    "D13S317": [11, 12],
                    "D16S539": [9, 11],
                    "D2S1338": [19, 23],
                    "D19S433": [14, 15.2],
                    "vWA": [16, 18],
                    "TPOX": [8, 8],
                    "D18S51": [12, 17],
                    "D5S818": [11, 13],
                    "FGA": [21, 24]
                }
            },
            "candidate_entity": "person-rakesh",
            "comparison_result": "Consistent Profile / Strong Association",
            "match_confidence": 0.94,
            "status": "Analyzed / Verified",
            "chain_of_custody_id": "COC-DEL-2026-001",
            "investigative_implication": "Corroborates physical presence of Rakesh Kumar inside conveyance DL 01 AB 9921."
        },
        {
            "report_id": "DNA-FSL-DEL-2026-402",
            "category": "DNA_BIOLOGICAL",
            "evidence_id": "EVID-DNA-002",
            "case_id": CASE_ID,
            "laboratory": "Biology Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T16:15:00Z",
            "evidence_item": "Hair Strand with Intact Follicle — Vehicle Rear Footwell Carpet",
            "examiner": "Senior Scientific Officer Dr. Meenakshi Sundaram",
            "examiner_badge": "FSL-BIO-042",
            "sample_id": "SMPL-BIO-DEL-402-B",
            "sample_type": "Hair Follicle with Root Sheath",
            "biological_material": "Human hair root sheath cellular material",
            "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate, Delhi",
            "collection_timestamp": "2026-09-03T11:45:00Z",
            "collection_method": "Fine forceps recovery into sterile glassine envelope",
            "dna_profile_id": "PROF-STR-DEL-9913",
            "str_profile_metadata": {
                "kit_used": "AmpFlSTR Identifiler Plus",
                "amelogenin": ["X", "X"],
                "loci_count": 16,
                "concordance_rate": "15/16 loci concordant with reference sample"
            },
            "candidate_entity": "person-priya",
            "comparison_result": "Investigative Lead / Potential Association",
            "match_confidence": 0.87,
            "status": "Analyzed / Corroborating Evidence",
            "chain_of_custody_id": "COC-DEL-2026-002",
            "investigative_implication": "Strongly corroborates Priya Sharma was transported inside vehicle DL 01 AB 9921."
        },
        {
            "report_id": "DNA-FSL-DEL-2026-403",
            "category": "DNA_BIOLOGICAL",
            "evidence_id": "EVID-DNA-003",
            "case_id": CASE_ID,
            "laboratory": "Biology Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T17:00:00Z",
            "evidence_item": "Discarded Cigarette Butt — ISBT Gate 2 Roadside Verge",
            "examiner": "Senior Scientific Officer Dr. Meenakshi Sundaram",
            "examiner_badge": "FSL-BIO-042",
            "sample_id": "SMPL-BIO-DEL-403-C",
            "sample_type": "Saliva Residue on Paper Filter",
            "biological_material": "Saliva epithelial residue",
            "collection_location": "ISBT Kashmere Gate Departure Gate 2 Verge, Delhi",
            "collection_timestamp": "2026-09-03T09:15:00Z",
            "collection_method": "Clean metal forceps in sterile tamper-evident vial",
            "dna_profile_id": "PROF-STR-DEL-9914",
            "str_profile_metadata": {
                "kit_used": "AmpFlSTR Identifiler Plus",
                "amelogenin": ["X", "Y"],
                "profile_status": "Partial Male Profile (8 loci resolved)"
            },
            "candidate_entity": None,
            "comparison_result": "Inconclusive / Unmatched Third-Party Profile",
            "match_confidence": 0.52,
            "status": "Requires Human Review / No Known Association",
            "chain_of_custody_id": "COC-DEL-2026-003",
            "investigative_implication": "Exclusionary sample; profile does not match Rakesh Kumar or Vikram Singh."
        },

        # CATEGORY 2: FINGERPRINT / LATENT PRINT EVIDENCE
        {
            "report_id": "FP-FSL-DEL-2026-218",
            "category": "FINGERPRINT_LATENT",
            "evidence_id": "EVID-FP-001",
            "case_id": CASE_ID,
            "laboratory": "Fingerprint Bureau, Crime Branch, Delhi Police",
            "examination_date": "2026-09-04T10:30:00Z",
            "evidence_item": "Passenger Door Interior Grab Handle — Vehicle DL 01 AB 9921",
            "examiner": "Fingerprint Expert Inspector K.S. Rathore",
            "examiner_badge": "FPB-EXP-112",
            "fingerprint_id": "FP-LAT-DEL-218-A",
            "surface_or_object": "Textured plastic interior door pull handle",
            "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
            "collection_timestamp": "2026-09-03T10:15:00Z",
            "print_quality": "High (14 unambiguous ridge minutiae points identified)",
            "print_type": "Latent Right Index Fingerprint (Accidental Whorl-Loop transition)",
            "candidate_entity": "person-rakesh",
            "similarity_score": 0.91,
            "comparison_result": "Strong Association / AFIS Match",
            "status": "Verified / Match Confirmed",
            "chain_of_custody_id": "COC-DEL-2026-004",
            "investigative_implication": "Direct physical contact established between Rakesh Kumar and vehicle cabin."
        },
        {
            "report_id": "FP-FSL-DEL-2026-219",
            "category": "FINGERPRINT_LATENT",
            "evidence_id": "EVID-FP-002",
            "case_id": CASE_ID,
            "laboratory": "Fingerprint Bureau, Crime Branch, Delhi Police",
            "examination_date": "2026-09-04T11:15:00Z",
            "evidence_item": "Steering Wheel Rim (9 O'Clock Position) — Vehicle DL 01 AB 9921",
            "examiner": "Fingerprint Expert Inspector K.S. Rathore",
            "examiner_badge": "FPB-EXP-112",
            "fingerprint_id": "FP-LAT-DEL-219-B",
            "surface_or_object": "Polyurethane steering wheel rim",
            "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
            "collection_timestamp": "2026-09-03T10:30:00Z",
            "print_quality": "High (15 minutiae points)",
            "print_type": "Latent Left Thumb Print (Plain Arch)",
            "candidate_entity": "person-vikram",
            "similarity_score": 0.94,
            "comparison_result": "Verified Operator Print",
            "status": "Verified / Driver Identity Confirmed",
            "chain_of_custody_id": "COC-DEL-2026-005",
            "investigative_implication": "Confirms Vikram Singh operated the conveyance during the incident timeframe."
        },
        {
            "report_id": "FP-FSL-DEL-2026-220",
            "category": "FINGERPRINT_LATENT",
            "evidence_id": "EVID-FP-003",
            "case_id": CASE_ID,
            "laboratory": "Fingerprint Bureau, Crime Branch, Delhi Police",
            "examination_date": "2026-09-04T12:00:00Z",
            "evidence_item": "Toll Receipt Paper Stub — Dashboard Console",
            "examiner": "Fingerprint Expert Inspector K.S. Rathore",
            "examiner_badge": "FPB-EXP-112",
            "fingerprint_id": "FP-LAT-DEL-220-C",
            "surface_or_object": "Thermal paper toll receipt",
            "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
            "collection_timestamp": "2026-09-03T10:45:00Z",
            "print_quality": "Low / Partial Smudge (5 minutiae points)",
            "print_type": "Indeterminate partial friction ridge impression",
            "candidate_entity": "person-rakesh",
            "similarity_score": 0.61,
            "comparison_result": "Inconclusive / Insufficient Minutiae for Conclusive Attribution",
            "status": "Inconclusive / Requires Secondary Examination",
            "chain_of_custody_id": "COC-DEL-2026-006",
            "investigative_implication": "Partial ridge flow consistent with Rakesh Kumar, but insufficient points for legal certainty."
        },

        # CATEGORY 3: MOBILE / DIGITAL FORENSICS
        {
            "report_id": "DIG-FSL-DEL-2026-309",
            "category": "DIGITAL_FORENSICS",
            "evidence_id": "EVID-DIG-001",
            "case_id": CASE_ID,
            "laboratory": "Cyber Forensics Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T12:30:00Z",
            "evidence_item": "Mobile Device Physical Extraction — Handset Samsung Galaxy A52",
            "examiner": "Forensic Scientist Rajesh Chawla",
            "examiner_badge": "FSL-CYB-048",
            "device_id": "DEV-SAMSUNG-A52-RAKESH",
            "imei": RAKESH_IMEI,
            "sim_identifier": "8991004450192801920",
            "artifact_id": "ART-GPS-GEO-881",
            "artifact_type": "GPS Waypoint & Location Breadcrumb Artifact",
            "application_source": "Google Location History Cache (gservices.db / SQLite)",
            "recovered_data_type": "Hardware GPS Fix with DOP accuracy 4.2m",
            "timestamp": "2026-09-02T21:40:12Z",
            "location_gps": {
                "latitude": 28.6675,
                "longitude": 77.2289,
                "accuracy_meters": 4.2,
                "altitude_meters": 218.4,
                "geofence_name": "ISBT Kashmere Gate Departure Outer Lane"
            },
            "associated_phone": RAKESH_PHONE,
            "associated_entity": "person-rakesh",
            "file_metadata": {
                "database_table": "location_history",
                "record_offset": "0x004F1820",
                "utc_timestamp_epoch": 1788385212
            },
            "extraction_method": "JTAG / Physical Chip Extraction (Cellebrite UFED)",
            "extraction_date": "2026-09-04T09:30:00Z",
            "forensic_tool": "Cellebrite UFED Physical Analyzer v7.68.2",
            "analyst": "Forensic Scientist Rajesh Chawla",
            "confidence": 0.94,
            "status": "Corroborating Evidence / Verified Waypoint",
            "investigative_implication": "Independently corroborates Rakesh Kumar's physical presence at ISBT departure curb at 21:40."
        },
        {
            "report_id": "DIG-FSL-DEL-2026-310",
            "category": "DIGITAL_FORENSICS",
            "evidence_id": "EVID-DIG-002",
            "case_id": CASE_ID,
            "laboratory": "Cyber Forensics Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T14:10:00Z",
            "evidence_item": "Mobile Handset Logical Acquisition — Xiaomi Redmi Note 10",
            "examiner": "Forensic Scientist Rajesh Chawla",
            "examiner_badge": "FSL-CYB-048",
            "device_id": "DEV-REDMI-NOTE10-VIKRAM",
            "imei": "861942049182301",
            "sim_identifier": "8991004104928172011",
            "artifact_id": "ART-MSG-SIG-402",
            "artifact_type": "Decrypted Instant Message Cache",
            "application_source": "Signal Private Messenger (org.thoughtcrime.securesms / database WAL)",
            "recovered_data_type": "Deleted encrypted message fragment recovered from unallocated flash blocks",
            "timestamp": "2026-09-02T21:52:45Z",
            "associated_phone": VIKRAM_PHONE,
            "associated_entity": "person-vikram",
            "file_metadata": {
                "sender": "Self (+91 97115 88201)",
                "recipient": "+91 98710 44219",
                "message_body": "Crossed outer ring road. Heading to Singhu toll. Switch off GPS now.",
                "delivery_receipt": "DELIVERED_READ"
            },
            "extraction_method": "Advanced Logical Extraction via MSAB XRY v10.4",
            "extraction_date": "2026-09-04T11:00:00Z",
            "forensic_tool": "MSAB XRY Logical Analyzer v10.4",
            "analyst": "Forensic Scientist Rajesh Chawla",
            "confidence": 0.91,
            "status": "Corroborating Evidence / Key Coordination Artifact",
            "investigative_implication": "Provides incontrovertible evidence of conspiratorial vehicular transit toward Singhu Border."
        },
        {
            "report_id": "DIG-FSL-DEL-2026-311",
            "category": "DIGITAL_FORENSICS",
            "evidence_id": "EVID-DIG-003",
            "case_id": CASE_ID,
            "laboratory": "Cyber Forensics Division, Forensic Science Laboratory, Rohini, Delhi",
            "examination_date": "2026-09-04T14:45:00Z",
            "evidence_item": "Payment App Cache File — Samsung Galaxy A52",
            "examiner": "Forensic Scientist Rajesh Chawla",
            "examiner_badge": "FSL-CYB-048",
            "device_id": "DEV-SAMSUNG-A52-RAKESH",
            "artifact_id": "ART-APP-UPI-991",
            "artifact_type": "Financial Application Local Transaction Ledger",
            "application_source": "Google Pay SQLite Database (com.google.android.apps.nbu.paisa.user)",
            "recovered_data_type": "Offline transaction pending record",
            "timestamp": "2026-09-02T22:02:18Z",
            "associated_phone": RAKESH_PHONE,
            "associated_entity": "bank-mule-01",
            "file_metadata": {
                "txn_ref": "UPI/202609022202/9841",
                "counterparty_vpa": "rkenterprises@okhdfc",
                "amount": 45000.00,
                "status": "COMPLETED_ATM_DISPENSED"
            },
            "extraction_method": "Physical Partition Dump",
            "extraction_date": "2026-09-04T11:30:00Z",
            "forensic_tool": "Cellebrite UFED Physical Analyzer",
            "analyst": "Forensic Scientist Rajesh Chawla",
            "confidence": 0.92,
            "status": "Financial Corroboration",
            "investigative_implication": "Directly links physical handset to rapid ₹45,000 cash withdrawal at Civil Lines ATM."
        },

        # CATEGORY 4: CCTV / VIDEO FORENSICS
        {
            "report_id": "VID-FSL-DEL-2026-552",
            "category": "CCTV_VIDEO_FORENSICS",
            "evidence_id": "EVID-VID-001",
            "case_id": CASE_ID,
            "laboratory": "Video Analytics & Digital Audio-Visual Division, FSL Rohini",
            "examination_date": "2026-09-04T13:30:00Z",
            "evidence_item": "DVR Video Footage Enhancement — ISBT Departure Concourse",
            "examiner": "Senior Scientific Officer S.K. Verma",
            "examiner_badge": "FSL-VID-081",
            "cctv_event_id": "VID-EVT-ISBT-GATE2-881",
            "camera_id": "CAM-ISBT-EXT-09",
            "timestamp": "2026-09-02T21:42:15Z",
            "location": "loc-kashmere-gate",
            "detected_person": "Male adult, estimated height 176cm, medium build, baseball cap",
            "candidate_entity": "person-rakesh",
            "person_similarity_score": 0.81,
            "detected_vehicle": "White compact sedan (Maruti Suzuki Swift Dzire)",
            "vehicle_similarity_score": 0.89,
            "partial_plate": "DL 01 AB **21",
            "clothing_attributes": "Dark grey nylon windcheater, blue denim trousers, dark sports shoes",
            "movement_direction": "Departing platform concourse toward kerbside bay 4",
            "entry_exit_info": "Subject observed escorting female subject toward rear passenger door at 21:42:40Z",
            "frame_reference": "FRM-CAM09-20260902-138402",
            "analyst_or_system": "Forensic Super-Resolution & Person Re-Identification Pipeline (DeepFace / OpenCV)",
            "comparison_result": "Investigative Lead / Visual Re-identification Match",
            "confidence": 0.81,
            "status": "Corroborating Evidence / Visual Placement",
            "investigative_implication": "Corroborates joint boarding of vehicle DL 01 AB 9921 at ISBT Kashmere Gate."
        },
        {
            "report_id": "VID-FSL-DEL-2026-553",
            "category": "CCTV_VIDEO_FORENSICS",
            "evidence_id": "EVID-VID-002",
            "case_id": CASE_ID,
            "laboratory": "Video Analytics & Digital Audio-Visual Division, FSL Rohini",
            "examination_date": "2026-09-04T14:00:00Z",
            "evidence_item": "ANPR High-Speed Camera Feed — NH-44 Singhu Toll Plaza",
            "examiner": "Senior Scientific Officer S.K. Verma",
            "examiner_badge": "FSL-VID-081",
            "cctv_event_id": "VID-EVT-SINGHU-LANE4-102",
            "camera_id": "ANPR-LANE-04",
            "timestamp": "2026-09-02T22:15:32Z",
            "location": "loc-singhu-border",
            "detected_vehicle": "Maruti Suzuki Swift Dzire, Commercial White Plate",
            "vehicle_similarity_score": 0.98,
            "partial_plate": "DL 01 AB 9921",
            "detected_person": "Driver profile behind windshield; rear cabin silhouette visible",
            "candidate_entity": "vehicle-dl01-9921",
            "person_similarity_score": 0.74,
            "clothing_attributes": "Light colored collar shirt on driver",
            "movement_direction": "Northbound proceeding towards Sonipat, Haryana",
            "entry_exit_info": "Fastag lane boom barrier elevated at 22:15:38Z",
            "frame_reference": "FRM-ANPR04-20260902-881290",
            "analyst_or_system": "Toll ANPR Optical Character Reader & Frame Enhancement Suite",
            "comparison_result": "Confirmed Vehicle Passage / Potential Driver Association",
            "confidence": 0.94,
            "status": "Confirmed Passage / Inter-State Transit",
            "investigative_implication": "Proves vehicle crossed out of Delhi jurisdiction 33 minutes after boarding at ISBT."
        },

        # CATEGORY 5: TRACE EVIDENCE
        {
            "report_id": "TRC-FSL-DEL-2026-114",
            "category": "TRACE_EVIDENCE",
            "evidence_id": "EVID-TRC-001",
            "case_id": CASE_ID,
            "laboratory": "Chemistry & Toxicology Division, FSL Rohini, Delhi",
            "examination_date": "2026-09-04T14:30:00Z",
            "evidence_item": "Soil Mineralogy Crusting — Vehicle Right Rear Wheel Arch",
            "examiner": "Senior Scientific Officer Dr. R.P. Nair",
            "examiner_badge": "FSL-CHM-053",
            "trace_type": "Soil Mineralogy & Petrographic Particulates",
            "sample_id": "SMPL-SOIL-DEL-114-A",
            "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate, Delhi",
            "collection_timestamp": "2026-09-03T12:00:00Z",
            "material_characteristics": "Sandy-loam clay enriched with fly-ash microspheres and heavy diesel hydrocarbons characteristic of industrial roadworks",
            "comparison_candidate": "Singhu Border NH-44 Toll Bypass Unpaved Shoulder Soil",
            "comparison_result": "Strong Association / Geochemical Mineral Concordance",
            "similarity_confidence": 0.88,
            "status": "Corroborating Evidence / Environmental Concordance",
            "chain_of_custody_id": "COC-DEL-2026-007",
            "investigative_implication": "Physical soil matrix on vehicle wheels matches unique geologic profile of Singhu Border highway verge."
        },
        {
            "report_id": "TRC-FSL-DEL-2026-115",
            "category": "TRACE_EVIDENCE",
            "evidence_id": "EVID-TRC-002",
            "case_id": CASE_ID,
            "laboratory": "Physics Division, FSL Rohini, Delhi",
            "examination_date": "2026-09-04T15:00:00Z",
            "evidence_item": "Bumper Paint Smear Transfer — Vehicle Left Front Bumper Corner",
            "examiner": "Scientific Officer Sunita Rao",
            "examiner_badge": "FSL-PHY-029",
            "trace_type": "Automotive Paint Transfer Smear",
            "sample_id": "SMPL-PNT-DEL-115-B",
            "collection_location": "Vehicle Left Front Bumper, PS Kashmere Gate",
            "collection_timestamp": "2026-09-03T12:15:00Z",
            "material_characteristics": "Yellow alkyd enamel paint smear over automobile polyurethane clearcoat",
            "comparison_candidate": "ISBT Kashmere Gate Platform 4 Bollard Paint",
            "comparison_result": "Consistent Multi-Layer Spectral Match (FTIR / Py-GC-MS)",
            "similarity_confidence": 0.87,
            "status": "Corroborating Evidence / Terminal Contact",
            "chain_of_custody_id": "COC-DEL-2026-008",
            "investigative_implication": "Vehicle made direct contact with bus terminal bollard barrier during pickup maneuver."
        },
        {
            "report_id": "TRC-FSL-DEL-2026-116",
            "category": "TRACE_EVIDENCE",
            "evidence_id": "EVID-TRC-003",
            "case_id": CASE_ID,
            "laboratory": "Chemistry & Toxicology Division, FSL Rohini, Delhi",
            "examination_date": "2026-09-04T15:30:00Z",
            "evidence_item": "Textile Fiber Sample — Front Passenger Headrest",
            "examiner": "Senior Scientific Officer Dr. R.P. Nair",
            "examiner_badge": "FSL-CHM-053",
            "trace_type": "Synthetic Fiber Fragment",
            "sample_id": "SMPL-FBR-DEL-116-C",
            "collection_location": "Front Passenger Headrest, Vehicle DL 01 AB 9921",
            "collection_timestamp": "2026-09-03T12:30:00Z",
            "material_characteristics": "Blue polyester staple fiber with circular cross section and titanium dioxide delustering pigment",
            "comparison_candidate": "Subject Reported Clothing Reference (Pure Silk Blend)",
            "comparison_result": "Non-Matching / Exclusionary Fiber (Generic Commercial Upholstery)",
            "similarity_confidence": 0.28,
            "status": "Exclusionary Finding / Non-Evidentiary",
            "chain_of_custody_id": "COC-DEL-2026-009",
            "investigative_implication": "Exclusionary trace; fiber originates from standard commercial aftermarket seat cover."
        },

        # CATEGORY 6: FOOTWEAR / TIRE IMPRESSION EVIDENCE
        {
            "report_id": "IMP-FSL-DEL-2026-607",
            "category": "FOOTWEAR_TIRE_IMPRESSIONS",
            "evidence_id": "EVID-IMP-001",
            "case_id": CASE_ID,
            "laboratory": "Impression Bureau, Crime Branch, Delhi Police",
            "examination_date": "2026-09-04T11:00:00Z",
            "evidence_item": "Electrostatic Dust Lifting & Dental Stone Cast — Tire Impression",
            "examiner": "Impression Specialist Inspector M.K. Yadav",
            "examiner_badge": "FPB-IMP-066",
            "impression_id": "IMP-TIRE-DEL-607-A",
            "impression_type": "Tire Tread Impression in Soft Alluvial Soil",
            "scene_location": "Muddy Verge beside ISBT Kashmere Gate Departure Gate 2",
            "timestamp": "2026-09-03T09:40:00Z",
            "pattern_characteristics": "4 longitudinal continuous zigzag ribs with lateral sipes and asymmetric variable-pitch tread blocks",
            "size_dimensions": "Tread footprint width 162mm, rib spacing 28mm",
            "tread_characteristics": "Bridgestone B290 165/80 R14 radial tire with localized 4mm circular stone retention cut in groove 2",
            "candidate_vehicle_or_person": "vehicle-dl01-9921",
            "comparison_result": "Strong Match / Individualizing Tread Defect Present",
            "similarity_score": 0.89,
            "confidence": 0.89,
            "status": "Corroborating Evidence / Scene Vehicle Placement",
            "chain_of_custody_id": "COC-DEL-2026-010",
            "investigative_implication": "Physical tire print at scene matches vehicle DL 01 AB 9921 right front wheel with individualizing cut defect."
        },
        {
            "report_id": "IMP-FSL-DEL-2026-608",
            "category": "FOOTWEAR_TIRE_IMPRESSIONS",
            "evidence_id": "EVID-IMP-002",
            "case_id": CASE_ID,
            "laboratory": "Impression Bureau, Crime Branch, Delhi Police",
            "examination_date": "2026-09-04T11:45:00Z",
            "evidence_item": "Dental Stone Cast — Footwear Impression",
            "examiner": "Impression Specialist Inspector M.K. Yadav",
            "examiner_badge": "FPB-IMP-066",
            "impression_id": "IMP-SHOE-DEL-608-B",
            "impression_type": "Footwear Outsole Impression in Damp Mud",
            "scene_location": "Kerbside verge near passenger boarding point, ISBT Gate 2",
            "timestamp": "2026-09-03T09:50:00Z",
            "pattern_characteristics": "Hexagonal perimeter perimeter tread with center chevron pivot and horizontal heel siping",
            "size_dimensions": "Outsole total length 294mm, ball width 106mm (Approx UK/India Size 9)",
            "tread_characteristics": "Woodland outdoor casual footwear sole with moderate lateral heel erosion wear",
            "candidate_vehicle_or_person": "person-rakesh",
            "comparison_result": "Investigative Lead / Class Characteristic & Wear Pattern Concordance",
            "similarity_score": 0.74,
            "confidence": 0.74,
            "status": "Investigative Lead / Physical Footprint Corroboration",
            "chain_of_custody_id": "COC-DEL-2026-011",
            "investigative_implication": "Shoe print pattern and size at scene is consistent with Rakesh Kumar's physical profile."
        },

        # CATEGORY 7: BALLISTICS / TOOLMARKS
        {
            "report_id": "BAL-FSL-DEL-2026-083",
            "category": "BALLISTICS_TOOLMARKS",
            "evidence_id": "EVID-BAL-001",
            "case_id": CASE_ID,
            "laboratory": "Ballistics & Toolmarks Division, FSL Rohini, Delhi",
            "examination_date": "2026-09-04T16:00:00Z",
            "evidence_item": "Brass Padlock & Shackle Assembly — Majnu Ka Tilla Transit Lodge Room 204",
            "examiner": "Senior Scientific Officer K.K. Bansal",
            "examiner_badge": "FSL-BAL-017",
            "item_id": "TOOL-PADLOCK-DEL-083-A",
            "evidence_type": "Toolmark Striation Impression / Forced Entry Scraping",
            "tool_or_weapon_type": "Flat-Blade Steel Pry Lever / Heavy Screwdriver (tip width 8.5mm)",
            "markings": "Striated microscopic scrape lines along brass shackle casing edge",
            "pattern_characteristics": "12 parallel micro-ridges created by hardened carbon steel tool with chipped corner bevel",
            "recovered_location": "Majnu Ka Tilla Transit Lodge Room 204, Delhi",
            "candidate_tool": "Steel Multi-Tool Pry Lever recovered from boot of vehicle DL 01 AB 9921",
            "comparison_result": "Potential Match / Microscopic Striation Concordance",
            "similarity_confidence": 0.78,
            "status": "Investigative Lead / Physical Tool Association",
            "chain_of_custody_id": "COC-DEL-2026-012",
            "investigative_implication": "Toolmark on lodge padlock matches microscopic defects of multi-tool found in Vikram's taxi boot."
        },
        {
            "report_id": "BAL-FSL-DEL-2026-084",
            "category": "BALLISTICS_TOOLMARKS",
            "evidence_id": "EVID-BAL-002",
            "case_id": CASE_ID,
            "laboratory": "Ballistics & Toolmarks Division, FSL Rohini, Delhi",
            "examination_date": "2026-09-04T16:30:00Z",
            "evidence_item": "Vehicle Identification Number (VIN) Stamping Inspection",
            "examiner": "Senior Scientific Officer K.K. Bansal",
            "examiner_badge": "FSL-BAL-017",
            "item_id": "TOOL-CHASSIS-DEL-084-B",
            "evidence_type": "Chassis Stamping Verification & Serial Number Integrity",
            "tool_or_weapon_type": "Factory Hydraulic Pin-Stamping Machine",
            "markings": "Chassis Plate Stamping: MA3EKB01S0091283",
            "pattern_characteristics": "Factory dot-matrix punch depth and spacing strictly conforms to Maruti Suzuki OEM production standards",
            "recovered_location": "Engine Firewall, Vehicle DL 01 AB 9921",
            "candidate_tool": "Maruti Suzuki Manesar Assembly Plant Tooling",
            "comparison_result": "Genuine Factory Stamping / Zero Secondary Alteration Detected",
            "similarity_confidence": 0.96,
            "status": "Verified / Authentic Vehicle Identity",
            "chain_of_custody_id": "COC-DEL-2026-013",
            "investigative_implication": "Chassis number is genuine and has not been ground off, re-punched, or cloned."
        },

        # CATEGORY 8: CHAIN OF CUSTODY & EVIDENCE INTEGRITY
        {
            "report_id": "COC-FSL-DEL-2026-901",
            "category": "CHAIN_OF_CUSTODY",
            "evidence_id": "EVID-COC-MASTER-001",
            "case_id": CASE_ID,
            "laboratory": "Central Evidence Management & Provenance Division, Delhi Police & FSL Rohini",
            "examination_date": "2026-09-05T10:00:00Z",
            "evidence_item": "Master Evidence Custody Ledger & BSA 2023 Section 63 Verification Record",
            "examiner": "Evidence Custodian Inspector Ramesh Chandra",
            "examiner_badge": "DP-CUS-019",
            "chain_of_custody_records": [
                {
                    "chain_of_custody_id": "COC-DEL-2026-001",
                    "evidence_id": "EVID-DNA-001",
                    "case_id": CASE_ID,
                    "collection_officer": "Sub-Inspector Anand Kumar",
                    "collection_officer_badge": "DP-SI-4921",
                    "collection_timestamp": "2026-09-03T11:30:00Z",
                    "collection_location": "PS Kashmere Gate Forensic Bay",
                    "transfer_events": [
                        {
                            "transfer_index": 1,
                            "transferred_by": "SI Anand Kumar",
                            "transferred_by_badge": "DP-SI-4921",
                            "transferred_to": "Evidence Custodian ASI Balraj Singh",
                            "transferred_to_badge": "DP-MAL-084",
                            "transfer_timestamp": "2026-09-03T13:00:00Z",
                            "purpose": "Secure Sealing in Tamper-Evident Evidence Bag",
                            "custody_status": "SEALED_IN_TRANSIT"
                        },
                        {
                            "transfer_index": 2,
                            "transferred_by": "ASI Balraj Singh",
                            "transferred_by_badge": "DP-MAL-084",
                            "transferred_to": "FSL Rohini Sample Receiving Division (Official Courier HC Vinod)",
                            "transferred_to_badge": "DP-COU-302",
                            "transfer_timestamp": "2026-09-03T15:30:00Z",
                            "purpose": "Transfer to Forensic Laboratory for DNA Extraction",
                            "custody_status": "LAB_RECEIVED"
                        },
                        {
                            "transfer_index": 3,
                            "transferred_by": "FSL Reception Clerk",
                            "transferred_by_badge": "FSL-REC-011",
                            "transferred_to": "Senior Scientific Officer Dr. Meenakshi Sundaram",
                            "transferred_to_badge": "FSL-BIO-042",
                            "transfer_timestamp": "2026-09-04T09:00:00Z",
                            "purpose": "Forensic STR DNA Profiling",
                            "custody_status": "UNDER_EXAMINATION"
                        },
                        {
                            "transfer_index": 4,
                            "transferred_by": "Dr. Meenakshi Sundaram",
                            "transferred_by_badge": "FSL-BIO-042",
                            "transferred_to": "Central Evidence Storage Vault (FSL Malkhana)",
                            "transferred_to_badge": "FSL-MAL-001",
                            "transfer_timestamp": "2026-09-04T18:00:00Z",
                            "purpose": "Cryo-preservation of DNA extract (-20 deg C)",
                            "custody_status": "PRESERVED_IN_VAULT"
                        }
                    ],
                    "storage_location": "Cold Storage Vault Rack B-12, FSL Rohini",
                    "examination_location": "DNA Lab 3, Biology Division, FSL Rohini",
                    "evidence_status": "ANALYZED_AND_SEALED",
                    "original_hash": "a4d8e9c12b7f3a5e8c0d1e2f4a6b8c0e2a4b6d8e0f2a4c6e8b0d2f4a6c8e0b2d",
                    "current_hash": "a4d8e9c12b7f3a5e8c0d1e2f4a6b8c0e2a4b6d8e0f2a4c6e8b0d2f4a6c8e0b2d",
                    "hash_algorithm": "SHA-256",
                    "integrity_status": "INTACT_VERIFIED",
                    "bsa_section_63_compliant": True,
                    "report_id": "DNA-FSL-DEL-2026-401"
                },
                {
                    "chain_of_custody_id": "COC-DEL-2026-004",
                    "evidence_id": "EVID-FP-001",
                    "case_id": CASE_ID,
                    "collection_officer": "Sub-Inspector Anand Kumar",
                    "collection_officer_badge": "DP-SI-4921",
                    "collection_timestamp": "2026-09-03T10:15:00Z",
                    "collection_location": "PS Kashmere Gate Forensic Bay",
                    "transfer_events": [
                        {
                            "transfer_index": 1,
                            "transferred_by": "SI Anand Kumar",
                            "transferred_by_badge": "DP-SI-4921",
                            "transferred_to": "Inspector K.S. Rathore",
                            "transferred_to_badge": "FPB-EXP-112",
                            "transfer_timestamp": "2026-09-03T14:00:00Z",
                            "purpose": "Latent Fingerprint Lifting & AFIS Digitization",
                            "custody_status": "HANDED_TO_EXAMINER"
                        },
                        {
                            "transfer_index": 2,
                            "transferred_by": "Inspector K.S. Rathore",
                            "transferred_by_badge": "FPB-EXP-112",
                            "transferred_to": "Crime Branch Evidence Locker",
                            "transferred_to_badge": "DP-MAL-084",
                            "transfer_timestamp": "2026-09-04T17:00:00Z",
                            "purpose": "Permanent Case Archival",
                            "custody_status": "ARCHIVED_SECURE"
                        }
                    ],
                    "storage_location": "Locker #402, Fingerprint Bureau, Crime Branch, Delhi",
                    "examination_location": "AFIS Terminal Room, Crime Branch",
                    "evidence_status": "ANALYZED_AND_SEALED",
                    "original_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
                    "current_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
                    "hash_algorithm": "SHA-256",
                    "integrity_status": "INTACT_VERIFIED",
                    "bsa_section_63_compliant": True,
                    "report_id": "FP-FSL-DEL-2026-218"
                }
            ],
            "status": "VERIFIED_INTACT_UNDER_BSA_2023",
            "investigative_implication": "Complete chain of custody unbroken; all seals intact from crime scene to FSL vault."
        }
    ]

    envelopes = []
    for rep in reports:
        env = create_envelope(
            source_type="FORENSIC",
            raw_content=rep,
            badge_id=rep.get("examiner_badge", "FSL-DEL-001"),
            record_id=f"REC-{rep['report_id']}"
        )
        envelopes.append(env)

        file_path = FORENSICS_DIR / f"{rep['report_id']}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(env, f, indent=2)

    print(f"[+] Successfully generated {len(reports)} comprehensive forensic reports across 8 categories in {FORENSICS_DIR}")
    return envelopes

if __name__ == "__main__":
    generate_forensic_expansion()
