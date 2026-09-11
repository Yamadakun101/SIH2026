"""
Script to apply the additive forensic expansion to data/dl-2026-0412.json
Preserves 100% of existing nodes, edges, entities, timeline, and provenance.
"""
import json
from pathlib import Path

DATA_FILE = Path("data/dl-2026-0412.json")

def expand_canonical_case():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Verify original counts
    orig_nodes = len(data["graph"]["elements"]["nodes"])
    orig_edges = len(data["graph"]["elements"]["edges"])
    orig_entities = len(data["entities"])
    orig_timeline = len(data["timeline"])
    orig_audit = len(data["provenance"]["audit_trail"])

    print(f"Original: {orig_nodes} nodes, {orig_edges} edges, {orig_entities} entities, {orig_timeline} events, {orig_audit} audit blocks.")

    # 2. Additive Nodes
    new_nodes = [
        {
            "data": {
                "id": "evidence-dna-touch-01",
                "label": "Touch DNA (Seatbelt Buckle)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "DNA_BIOLOGICAL_EVIDENCE",
                "centrality_score": 0.72,
                "risk_level": "CRITICAL",
                "evidence_count": 4,
                "icon": "dna",
                "category": "DNA_BIOLOGICAL",
                "sample_id": "SMPL-BIO-DEL-401-A",
                "candidate_entity": "person-rakesh",
                "comparison_result": "Consistent Profile / Strong Association",
                "confidence": 0.94,
                "report_id": "DNA-FSL-DEL-2026-401",
                "chain_of_custody_id": "COC-DEL-2026-001",
                "status": "VERIFIED_MATCH"
            }
        },
        {
            "data": {
                "id": "evidence-dna-hair-01",
                "label": "Hair Follicle (Rear Carpet)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "DNA_BIOLOGICAL_EVIDENCE",
                "centrality_score": 0.65,
                "risk_level": "HIGH",
                "evidence_count": 3,
                "icon": "dna",
                "category": "DNA_BIOLOGICAL",
                "sample_id": "SMPL-BIO-DEL-402-B",
                "candidate_entity": "person-priya",
                "comparison_result": "Investigative Lead / Potential Association",
                "confidence": 0.87,
                "report_id": "DNA-FSL-DEL-2026-402",
                "chain_of_custody_id": "COC-DEL-2026-002",
                "status": "CORROBORATING_FINDING"
            }
        },
        {
            "data": {
                "id": "evidence-fp-door-01",
                "label": "Latent Print (Passenger Door Handle)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "FINGERPRINT_EVIDENCE",
                "centrality_score": 0.78,
                "risk_level": "CRITICAL",
                "evidence_count": 5,
                "icon": "fingerprint",
                "category": "FINGERPRINT_LATENT",
                "fingerprint_id": "FP-LAT-DEL-218-A",
                "candidate_entity": "person-rakesh",
                "similarity_score": 0.91,
                "comparison_result": "Strong Association / AFIS Match",
                "confidence": 0.91,
                "report_id": "FP-FSL-DEL-2026-218",
                "chain_of_custody_id": "COC-DEL-2026-004",
                "status": "VERIFIED_MATCH"
            }
        },
        {
            "data": {
                "id": "evidence-fp-wheel-01",
                "label": "Latent Print (Steering Wheel)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "FINGERPRINT_EVIDENCE",
                "centrality_score": 0.71,
                "risk_level": "HIGH",
                "evidence_count": 4,
                "icon": "fingerprint",
                "category": "FINGERPRINT_LATENT",
                "fingerprint_id": "FP-LAT-DEL-219-B",
                "candidate_entity": "person-vikram",
                "similarity_score": 0.94,
                "comparison_result": "Verified Operator Print",
                "confidence": 0.94,
                "report_id": "FP-FSL-DEL-2026-219",
                "chain_of_custody_id": "COC-DEL-2026-005",
                "status": "VERIFIED_OPERATOR"
            }
        },
        {
            "data": {
                "id": "evidence-dig-gps-01",
                "label": "GPS Artifact (ISBT Departure Bay)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "DIGITAL_FORENSIC_ARTIFACT",
                "centrality_score": 0.76,
                "risk_level": "CRITICAL",
                "evidence_count": 4,
                "icon": "smartphone",
                "category": "DIGITAL_FORENSICS",
                "artifact_id": "ART-GPS-GEO-881",
                "associated_entity": "person-rakesh",
                "timestamp": "2026-09-02T21:40:12Z",
                "comparison_result": "Corroborating Evidence / Verified Waypoint",
                "confidence": 0.94,
                "report_id": "DIG-FSL-DEL-2026-309",
                "status": "VERIFIED_WAYPOINT"
            }
        },
        {
            "data": {
                "id": "evidence-dig-msg-01",
                "label": "Signal Chat Fragment (Ring Road -> Singhu)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "DIGITAL_FORENSIC_ARTIFACT",
                "centrality_score": 0.74,
                "risk_level": "HIGH",
                "evidence_count": 4,
                "icon": "message-square",
                "category": "DIGITAL_FORENSICS",
                "artifact_id": "ART-MSG-SIG-402",
                "associated_entity": "person-vikram",
                "timestamp": "2026-09-02T21:52:45Z",
                "comparison_result": "Corroborating Evidence / Key Coordination Artifact",
                "confidence": 0.91,
                "report_id": "DIG-FSL-DEL-2026-310",
                "status": "VERIFIED_COORDINATION"
            }
        },
        {
            "data": {
                "id": "evidence-vid-isbt-01",
                "label": "CCTV Re-ID (ISBT Platform Concourse)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "VIDEO_FORENSIC_EVIDENCE",
                "centrality_score": 0.69,
                "risk_level": "HIGH",
                "evidence_count": 5,
                "icon": "video",
                "category": "CCTV_VIDEO_FORENSICS",
                "cctv_event_id": "VID-EVT-ISBT-GATE2-881",
                "camera_id": "CAM-ISBT-EXT-09",
                "timestamp": "2026-09-02T21:42:15Z",
                "candidate_entity": "person-rakesh",
                "comparison_result": "Investigative Lead / Visual Re-identification Match",
                "confidence": 0.81,
                "report_id": "VID-FSL-DEL-2026-552",
                "status": "VISUAL_CORROBORATION"
            }
        },
        {
            "data": {
                "id": "evidence-vid-singhu-01",
                "label": "High-Speed ANPR Crossing (Singhu NH-44)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "VIDEO_FORENSIC_EVIDENCE",
                "centrality_score": 0.77,
                "risk_level": "CRITICAL",
                "evidence_count": 4,
                "icon": "video",
                "category": "CCTV_VIDEO_FORENSICS",
                "cctv_event_id": "VID-EVT-SINGHU-LANE4-102",
                "camera_id": "ANPR-LANE-04",
                "timestamp": "2026-09-02T22:15:32Z",
                "candidate_entity": "vehicle-dl01-9921",
                "comparison_result": "Confirmed Vehicle Passage / Potential Driver Association",
                "confidence": 0.94,
                "report_id": "VID-FSL-DEL-2026-553",
                "status": "CONFIRMED_PASSAGE"
            }
        },
        {
            "data": {
                "id": "evidence-trace-soil-01",
                "label": "Wheel Arch Soil Mineralogy Trace",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "TRACE_EVIDENCE",
                "centrality_score": 0.68,
                "risk_level": "HIGH",
                "evidence_count": 3,
                "icon": "layers",
                "category": "TRACE_EVIDENCE",
                "sample_id": "SMPL-SOIL-DEL-114-A",
                "comparison_result": "Strong Association / Geochemical Mineral Concordance",
                "confidence": 0.88,
                "report_id": "TRC-FSL-DEL-2026-114",
                "chain_of_custody_id": "COC-DEL-2026-007",
                "status": "GEOLOGIC_LINK"
            }
        },
        {
            "data": {
                "id": "evidence-trace-paint-01",
                "label": "Front Bumper Paint Smear (ISBT Bollard)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "TRACE_EVIDENCE",
                "centrality_score": 0.67,
                "risk_level": "HIGH",
                "evidence_count": 3,
                "icon": "layers",
                "category": "TRACE_EVIDENCE",
                "sample_id": "SMPL-PNT-DEL-115-B",
                "comparison_result": "Consistent Multi-Layer Spectral Match",
                "confidence": 0.87,
                "report_id": "TRC-FSL-DEL-2026-115",
                "chain_of_custody_id": "COC-DEL-2026-008",
                "status": "TERMINAL_CONTACT"
            }
        },
        {
            "data": {
                "id": "evidence-tire-isbt-01",
                "label": "Tire Tread Impression (ISBT Gate 2 Verge)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "IMPRESSION_EVIDENCE",
                "centrality_score": 0.73,
                "risk_level": "HIGH",
                "evidence_count": 3,
                "icon": "circle-dot",
                "category": "FOOTWEAR_TIRE_IMPRESSIONS",
                "impression_id": "IMP-TIRE-DEL-607-A",
                "candidate_vehicle_or_person": "vehicle-dl01-9921",
                "comparison_result": "Strong Match / Individualizing Tread Defect Present",
                "confidence": 0.89,
                "report_id": "IMP-FSL-DEL-2026-607",
                "chain_of_custody_id": "COC-DEL-2026-010",
                "status": "SCENE_VEHICLE_MATCH"
            }
        },
        {
            "data": {
                "id": "evidence-shoe-isbt-01",
                "label": "Footwear Outsole Impression (ISBT Gate 2)",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "IMPRESSION_EVIDENCE",
                "centrality_score": 0.63,
                "risk_level": "MEDIUM",
                "evidence_count": 3,
                "icon": "footprints",
                "category": "FOOTWEAR_TIRE_IMPRESSIONS",
                "impression_id": "IMP-SHOE-DEL-608-B",
                "candidate_vehicle_or_person": "person-rakesh",
                "comparison_result": "Investigative Lead / Class Characteristic Concordance",
                "confidence": 0.74,
                "report_id": "IMP-FSL-DEL-2026-608",
                "chain_of_custody_id": "COC-DEL-2026-011",
                "status": "INVESTIGATIVE_LEAD"
            }
        },
        {
            "data": {
                "id": "evidence-tool-latch-01",
                "label": "Lodge Padlock Striation Toolmark",
                "type": "FORENSIC_EVIDENCE",
                "sub_role": "TOOLMARK_EVIDENCE",
                "centrality_score": 0.61,
                "risk_level": "MEDIUM",
                "evidence_count": 3,
                "icon": "wrench",
                "category": "BALLISTICS_TOOLMARKS",
                "item_id": "TOOL-PADLOCK-DEL-083-A",
                "candidate_tool": "Steel Multi-Tool (Vehicle Boot)",
                "comparison_result": "Potential Match / Microscopic Striation Concordance",
                "confidence": 0.78,
                "report_id": "BAL-FSL-DEL-2026-083",
                "chain_of_custody_id": "COC-DEL-2026-012",
                "status": "POTENTIAL_TOOL_MATCH"
            }
        }
    ]

    existing_node_ids = {n["data"]["id"] for n in data["graph"]["elements"]["nodes"]}
    for node in new_nodes:
        if node["data"]["id"] not in existing_node_ids:
            data["graph"]["elements"]["nodes"].append(node)
            existing_node_ids.add(node["data"]["id"])

    # 3. Additive Edges
    new_edges = [
        # DNA Edges
        {
            "data": {
                "id": "edge-forensic-dna-01",
                "source": "evidence-dna-touch-01",
                "target": "person-rakesh",
                "label": "TOUCH_DNA_MATCH [94%]",
                "confidence": 0.94,
                "confidence_explanation": "16-loci autosomal STR profile concordant with reference sample of Rakesh Kumar.",
                "interaction_count": 1,
                "category": "FORENSIC_BIOLOGICAL"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dna-02",
                "source": "evidence-dna-touch-01",
                "target": "vehicle-dl01-9921",
                "label": "RECOVERED_FROM",
                "confidence": 0.98,
                "confidence_explanation": "Swabbed directly from passenger-side seatbelt buckle inside vehicle DL 01 AB 9921.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dna-03",
                "source": "evidence-dna-hair-01",
                "target": "person-priya",
                "label": "DNA_PROFILE_CONCORDANCE [87%]",
                "confidence": 0.87,
                "confidence_explanation": "Nuclear DNA extracted from hair follicle matches Priya Sharma reference profile across 15 loci.",
                "interaction_count": 1,
                "category": "FORENSIC_BIOLOGICAL"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dna-04",
                "source": "evidence-dna-hair-01",
                "target": "vehicle-dl01-9921",
                "label": "RECOVERED_FROM",
                "confidence": 0.98,
                "confidence_explanation": "Recovered from rear footwell passenger carpet during scene inspection.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },

        # Fingerprint Edges
        {
            "data": {
                "id": "edge-forensic-fp-01",
                "source": "evidence-fp-door-01",
                "target": "person-rakesh",
                "label": "LATENT_PRINT_MATCH [91%]",
                "confidence": 0.91,
                "confidence_explanation": "14 clear ridge minutiae points match Rakesh Kumar's right index fingerprint in AFIS.",
                "interaction_count": 1,
                "category": "FORENSIC_FINGERPRINT"
            }
        },
        {
            "data": {
                "id": "edge-forensic-fp-02",
                "source": "evidence-fp-door-01",
                "target": "vehicle-dl01-9921",
                "label": "LIFTED_FROM",
                "confidence": 0.99,
                "confidence_explanation": "Latent friction ridge print developed on passenger interior door handle.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },
        {
            "data": {
                "id": "edge-forensic-fp-03",
                "source": "evidence-fp-wheel-01",
                "target": "person-vikram",
                "label": "OPERATOR_PRINT_MATCH [94%]",
                "confidence": 0.94,
                "confidence_explanation": "15 minutiae points match Vikram Singh's left thumb plain arch impression.",
                "interaction_count": 1,
                "category": "FORENSIC_FINGERPRINT"
            }
        },
        {
            "data": {
                "id": "edge-forensic-fp-04",
                "source": "evidence-fp-wheel-01",
                "target": "vehicle-dl01-9921",
                "label": "LIFTED_FROM",
                "confidence": 0.99,
                "confidence_explanation": "Developed from polyurethane steering wheel rim at 9 o'clock grip position.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },

        # Digital Forensics Edges
        {
            "data": {
                "id": "edge-forensic-dig-01",
                "source": "evidence-dig-gps-01",
                "target": "person-rakesh",
                "label": "EXTRACTED_FROM_DEVICE",
                "confidence": 0.96,
                "confidence_explanation": "Recovered from JTAG physical partition dump of Samsung A52 handset carried by Rakesh.",
                "interaction_count": 1,
                "category": "DIGITAL_FORENSICS"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dig-02",
                "source": "evidence-dig-gps-01",
                "target": "loc-kashmere-gate",
                "label": "GPS_CO_LOCATION 21:40",
                "confidence": 0.94,
                "confidence_explanation": "Precision GPS coordinate fix (lat 28.6675, lng 77.2289) inside ISBT outer gate at 21:40:12Z.",
                "interaction_count": 1,
                "category": "LOCATION"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dig-03",
                "source": "evidence-dig-msg-01",
                "target": "person-vikram",
                "label": "SENT_BY_OPERATOR",
                "confidence": 0.92,
                "confidence_explanation": "Deleted Signal message cache fragment recovered from Vikram's Redmi handset unallocated blocks.",
                "interaction_count": 1,
                "category": "DIGITAL_FORENSICS"
            }
        },
        {
            "data": {
                "id": "edge-forensic-dig-04",
                "source": "evidence-dig-msg-01",
                "target": "phone-burner-rakesh",
                "label": "COORDINATION_RECIPIENT",
                "confidence": 0.91,
                "confidence_explanation": "Addressed to +91 98710 44219: 'Crossed outer ring road. Heading to Singhu toll.'",
                "interaction_count": 1,
                "category": "DIGITAL_FORENSICS"
            }
        },

        # CCTV / Video Forensics Edges
        {
            "data": {
                "id": "edge-forensic-vid-01",
                "source": "evidence-vid-isbt-01",
                "target": "person-rakesh",
                "label": "VISUAL_REID [81%]",
                "confidence": 0.81,
                "confidence_explanation": "Super-resolution facial & clothing re-identification match with Rakesh Kumar profile.",
                "interaction_count": 1,
                "category": "CCTV_ANPR"
            }
        },
        {
            "data": {
                "id": "edge-forensic-vid-02",
                "source": "evidence-vid-isbt-01",
                "target": "vehicle-dl01-9921",
                "label": "BOARDED_VEHICLE 21:43",
                "confidence": 0.89,
                "confidence_explanation": "Camera frame sequence captures boarding of white Swift Dzire at ISBT Kerbside Bay 4.",
                "interaction_count": 1,
                "category": "CCTV_ANPR"
            }
        },
        {
            "data": {
                "id": "edge-forensic-vid-03",
                "source": "evidence-vid-isbt-01",
                "target": "loc-kashmere-gate",
                "label": "RECORDED_AT",
                "confidence": 0.99,
                "confidence_explanation": "Captured on fixed overhead CCTV camera CAM-ISBT-EXT-09.",
                "interaction_count": 1,
                "category": "LOCATION"
            }
        },
        {
            "data": {
                "id": "edge-forensic-vid-04",
                "source": "evidence-vid-singhu-01",
                "target": "vehicle-dl01-9921",
                "label": "ANPR_CONFIRMED [98%]",
                "confidence": 0.98,
                "confidence_explanation": "NH-44 Singhu Toll high-speed camera optical character reader resolved DL 01 AB 9921.",
                "interaction_count": 1,
                "category": "CCTV_ANPR"
            }
        },
        {
            "data": {
                "id": "edge-forensic-vid-05",
                "source": "evidence-vid-singhu-01",
                "target": "loc-singhu-border",
                "label": "RECORDED_AT",
                "confidence": 0.99,
                "confidence_explanation": "Recorded at Singhu Toll Plaza Lane 4 northbound at 22:15:32Z.",
                "interaction_count": 1,
                "category": "LOCATION"
            }
        },

        # Trace Evidence Edges
        {
            "data": {
                "id": "edge-forensic-trc-01",
                "source": "evidence-trace-soil-01",
                "target": "vehicle-dl01-9921",
                "label": "DEPOSITED_ON",
                "confidence": 0.98,
                "confidence_explanation": "Recovered from mud build-up on right rear wheel arch of DL 01 AB 9921.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },
        {
            "data": {
                "id": "edge-forensic-trc-02",
                "source": "evidence-trace-soil-01",
                "target": "loc-singhu-border",
                "label": "MINERALOGY_CONCORDANCE [88%]",
                "confidence": 0.88,
                "confidence_explanation": "Petrographic analysis reveals fly-ash and sandy-loam ratios unique to Singhu Toll bypass works.",
                "interaction_count": 1,
                "category": "FORENSIC_TRACE"
            }
        },
        {
            "data": {
                "id": "edge-forensic-trc-03",
                "source": "evidence-trace-paint-01",
                "target": "vehicle-dl01-9921",
                "label": "SMEAR_ON_BUMPER",
                "confidence": 0.98,
                "confidence_explanation": "Automotive paint scuff sample lifted from front bumper corner.",
                "interaction_count": 1,
                "category": "CHAIN_OF_CUSTODY"
            }
        },
        {
            "data": {
                "id": "edge-forensic-trc-04",
                "source": "evidence-trace-paint-01",
                "target": "loc-kashmere-gate",
                "label": "BOLLARD_PAINT_MATCH [87%]",
                "confidence": 0.87,
                "confidence_explanation": "Py-GC-MS spectral signature matches yellow alkyd barrier enamel at ISBT Bay 4.",
                "interaction_count": 1,
                "category": "FORENSIC_TRACE"
            }
        },

        # Impression Edges
        {
            "data": {
                "id": "edge-forensic-imp-01",
                "source": "evidence-tire-isbt-01",
                "target": "vehicle-dl01-9921",
                "label": "TIRE_TREAD_MATCH [89%]",
                "confidence": 0.89,
                "confidence_explanation": "Bridgestone B290 tread pattern with localized stone cut defect matches right front tire.",
                "interaction_count": 1,
                "category": "FORENSIC_IMPRESSION"
            }
        },
        {
            "data": {
                "id": "edge-forensic-imp-02",
                "source": "evidence-tire-isbt-01",
                "target": "loc-kashmere-gate",
                "label": "RECOVERED_AT_SCENE",
                "confidence": 0.98,
                "confidence_explanation": "Cast made on muddy verge beside ISBT Gate 2 departure road.",
                "interaction_count": 1,
                "category": "LOCATION"
            }
        },
        {
            "data": {
                "id": "edge-forensic-imp-03",
                "source": "evidence-shoe-isbt-01",
                "target": "person-rakesh",
                "label": "OUTSOLE_WEAR_CONSISTENT [74%]",
                "confidence": 0.74,
                "confidence_explanation": "UK Size 9 outdoor shoe tread and lateral heel wear pattern consistent with Rakesh's gait.",
                "interaction_count": 1,
                "category": "FORENSIC_IMPRESSION"
            }
        },
        {
            "data": {
                "id": "edge-forensic-imp-04",
                "source": "evidence-shoe-isbt-01",
                "target": "loc-kashmere-gate",
                "label": "RECOVERED_AT_SCENE",
                "confidence": 0.98,
                "confidence_explanation": "Cast lifted from muddy ground beside passenger boarding curb.",
                "interaction_count": 1,
                "category": "LOCATION"
            }
        },

        # Toolmark Edges
        {
            "data": {
                "id": "edge-forensic-bal-01",
                "source": "evidence-tool-latch-01",
                "target": "vehicle-dl01-9921",
                "label": "TOOL_RECOVERED_FROM_BOOT [78%]",
                "confidence": 0.78,
                "confidence_explanation": "Micro-striations on lodge room padlock match defect on pry tool in vehicle boot.",
                "interaction_count": 1,
                "category": "FORENSIC_TOOLMARK"
            }
        }
    ]

    existing_edge_ids = {e["data"]["id"] for e in data["graph"]["elements"]["edges"]}
    for edge in new_edges:
        if edge["data"]["id"] not in existing_edge_ids:
            data["graph"]["elements"]["edges"].append(edge)
            existing_edge_ids.add(edge["data"]["id"])

    # 4. Additive Entity Dossiers in data["entities"]
    new_entities = {
        "evidence-dna-touch-01": {
            "id": "evidence-dna-touch-01",
            "type": "FORENSIC_EVIDENCE",
            "label": "Touch DNA (Seatbelt Buckle)",
            "aliases": ["DNA Sample 401-A"],
            "sub_role": "DNA_BIOLOGICAL_EVIDENCE",
            "attributes": {
                "category": "DNA_BIOLOGICAL",
                "biological_material": "Epithelial cellular material",
                "candidate_entity": "person-rakesh",
                "comparison_result": "Consistent Profile / Strong Association",
                "match_confidence": 0.94,
                "laboratory": "Biology Division, FSL Rohini, Delhi",
                "report_id": "DNA-FSL-DEL-2026-401"
            },
            "metrics": {
                "centrality_score": 0.72,
                "degree": 2,
                "betweenness": 0.48,
                "risk_level": "CRITICAL",
                "cluster_id": "syndicate-north-01"
            },
            "supporting_records": [
                "DNA-FSL-DEL-2026-401",
                "COC-DEL-2026-001"
            ],
            "provenance_hash": "a4d8e9c12b7f3a5e8c0d1e2f4a6b8c0e2a4b6d8e0f2a4c6e8b0d2f4a6c8e0b2d"
        },
        "evidence-fp-door-01": {
            "id": "evidence-fp-door-01",
            "type": "FORENSIC_EVIDENCE",
            "label": "Latent Print (Passenger Door Handle)",
            "aliases": ["Latent Print 218-A"],
            "sub_role": "FINGERPRINT_EVIDENCE",
            "attributes": {
                "category": "FINGERPRINT_LATENT",
                "surface": "Textured plastic interior door pull handle",
                "candidate_entity": "person-rakesh",
                "similarity_score": 0.91,
                "comparison_result": "Strong Association / AFIS Match",
                "laboratory": "Fingerprint Bureau, Crime Branch, Delhi Police",
                "report_id": "FP-FSL-DEL-2026-218"
            },
            "metrics": {
                "centrality_score": 0.78,
                "degree": 2,
                "betweenness": 0.54,
                "risk_level": "CRITICAL",
                "cluster_id": "syndicate-north-01"
            },
            "supporting_records": [
                "FP-FSL-DEL-2026-218",
                "COC-DEL-2026-004"
            ],
            "provenance_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8"
        },
        "evidence-trace-soil-01": {
            "id": "evidence-trace-soil-01",
            "type": "FORENSIC_EVIDENCE",
            "label": "Wheel Arch Soil Mineralogy Trace",
            "aliases": ["Soil Trace 114-A"],
            "sub_role": "TRACE_EVIDENCE",
            "attributes": {
                "category": "TRACE_EVIDENCE",
                "material": "Sandy-loam clay enriched with fly-ash microspheres",
                "comparison_target": "Singhu Border NH-44 Toll Bypass Unpaved Shoulder Soil",
                "similarity_confidence": 0.88,
                "laboratory": "Chemistry Division, FSL Rohini, Delhi",
                "report_id": "TRC-FSL-DEL-2026-114"
            },
            "metrics": {
                "centrality_score": 0.68,
                "degree": 2,
                "betweenness": 0.42,
                "risk_level": "HIGH",
                "cluster_id": "syndicate-north-01"
            },
            "supporting_records": [
                "TRC-FSL-DEL-2026-114",
                "COC-DEL-2026-007"
            ],
            "provenance_hash": "f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0"
        }
    }

    for ent_id, ent_val in new_entities.items():
        if ent_id not in data["entities"]:
            data["entities"][ent_id] = ent_val

    # Update existing entities' supporting_records additively
    if "person-rakesh" in data["entities"]:
        for rec in ["DNA-FSL-DEL-2026-401", "FP-FSL-DEL-2026-218", "DIG-FSL-DEL-2026-309", "IMP-FSL-DEL-2026-608"]:
            if rec not in data["entities"]["person-rakesh"]["supporting_records"]:
                data["entities"]["person-rakesh"]["supporting_records"].append(rec)

    if "vehicle-dl01-9921" in data["entities"]:
        for rec in ["DNA-FSL-DEL-2026-401", "FP-FSL-DEL-2026-218", "TRC-FSL-DEL-2026-114", "TRC-FSL-DEL-2026-115", "IMP-FSL-DEL-2026-607"]:
            if rec not in data["entities"]["vehicle-dl01-9921"]["supporting_records"]:
                data["entities"]["vehicle-dl01-9921"]["supporting_records"].append(rec)

    if "person-vikram" in data["entities"]:
        for rec in ["FP-FSL-DEL-2026-219", "DIG-FSL-DEL-2026-310"]:
            if rec not in data["entities"]["person-vikram"]["supporting_records"]:
                data["entities"]["person-vikram"]["supporting_records"].append(rec)

    # 5. Additive Timeline Events
    new_timeline_events = [
        {
            "event_id": "evt-005",
            "timestamp": "2026-09-03T09:40:00Z",
            "title": "Crime Scene Impression Casts Lifted",
            "category": "FORENSIC_INVESTIGATION",
            "source_record_id": "IMP-FSL-DEL-2026-607",
            "location": "ISBT Kashmere Gate Departure Gate 2 Verge",
            "involved_entities": ["vehicle-dl01-9921", "person-rakesh", "evidence-tire-isbt-01", "evidence-shoe-isbt-01"],
            "description": "Impression bureau specialists lifted dental stone casts of tire tread (B290 with stone cut defect) and footwear impression (UK 9 casual outdoor sole) from unpaved road verge.",
            "confidence": 0.89
        },
        {
            "event_id": "evt-006",
            "timestamp": "2026-09-03T11:30:00Z",
            "title": "Conveyance Forensic Swabbing & Latent Print Lifting",
            "category": "FORENSIC_INVESTIGATION",
            "source_record_id": "DNA-FSL-DEL-2026-401",
            "location": "Forensic Inspection Bay, PS Kashmere Gate",
            "involved_entities": ["vehicle-dl01-9921", "person-rakesh", "evidence-dna-touch-01", "evidence-fp-door-01"],
            "description": "Epithelial touch DNA swabbed from seatbelt buckle and high-definition latent prints lifted from passenger door handle inside vehicle DL 01 AB 9921.",
            "confidence": 0.94
        },
        {
            "event_id": "evt-007",
            "timestamp": "2026-09-04T12:30:00Z",
            "title": "JTAG Mobile Chip-Off Extraction & GPS Carving",
            "category": "CYBER_FORENSICS",
            "source_record_id": "DIG-FSL-DEL-2026-309",
            "location": "Cyber Forensics Lab, FSL Rohini",
            "involved_entities": ["phone-burner-rakesh", "person-rakesh", "evidence-dig-gps-01"],
            "description": "Forensic recovery of unallocated SQLite database carved physical GPS breadcrumbs placing burner handset at ISBT outer bay at 21:40 on 02-Sep.",
            "confidence": 0.94
        },
        {
            "event_id": "evt-008",
            "timestamp": "2026-09-04T15:30:00Z",
            "title": "FSL DNA STR Profile Verification & Match Released",
            "category": "BIOLOGICAL_FORENSICS",
            "source_record_id": "DNA-FSL-DEL-2026-401",
            "location": "Biology Division, FSL Rohini",
            "involved_entities": ["evidence-dna-touch-01", "person-rakesh", "vehicle-dl01-9921"],
            "description": "FSL Rohini Biology Division confirmed 16-loci autosomal STR profile match between seatbelt swab and Rakesh Kumar (0.94 match confidence).",
            "confidence": 0.94
        }
    ]

    existing_evt_ids = {e["event_id"] for e in data["timeline"]}
    for evt in new_timeline_events:
        if evt["event_id"] not in existing_evt_ids:
            data["timeline"].append(evt)
            existing_evt_ids.add(evt["event_id"])

    # Sort timeline chronologically
    data["timeline"] = sorted(data["timeline"], key=lambda x: x["timestamp"])

    # 6. Additive Provenance Audit Trail
    new_audit_blocks = [
        {
            "block_index": 5,
            "record_id": "DNA-FSL-DEL-2026-401",
            "sha256": "a4d8e9c12b7f3a5e8c0d1e2f4a6b8c0e2a4b6d8e0f2a4c6e8b0d2f4a6c8e0b2d",
            "timestamp": "2026-09-04T16:00:00Z",
            "officer_badge": "FSL-BIO-042",
            "status": "VALID"
        },
        {
            "block_index": 6,
            "record_id": "FP-FSL-DEL-2026-218",
            "sha256": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
            "timestamp": "2026-09-04T16:15:00Z",
            "officer_badge": "FPB-EXP-112",
            "status": "VALID"
        },
        {
            "block_index": 7,
            "record_id": "DIG-FSL-DEL-2026-309",
            "sha256": "d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4",
            "timestamp": "2026-09-04T16:30:00Z",
            "officer_badge": "FSL-CYB-048",
            "status": "VALID"
        },
        {
            "block_index": 8,
            "record_id": "TRC-FSL-DEL-2026-114",
            "sha256": "f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0",
            "timestamp": "2026-09-04T16:45:00Z",
            "officer_badge": "FSL-CHM-053",
            "status": "VALID"
        }
    ]

    existing_block_indices = {b["block_index"] for b in data["provenance"]["audit_trail"]}
    for block in new_audit_blocks:
        if block["block_index"] not in existing_block_indices:
            data["provenance"]["audit_trail"].append(block)
            existing_block_indices.add(block["block_index"])

    # Update metadata
    data["case_metadata"]["total_evidence_records"] = 104
    data["case_metadata"]["total_entities_identified"] = 23

    # 7. Add Dedicated Top-Level "forensics" Section Organizing All 8 Categories
    data["forensics"] = {
        "case_id": "DL-2026-0412",
        "total_forensic_records": 19,
        "categories_present": [
            "DNA_BIOLOGICAL",
            "FINGERPRINT_LATENT",
            "DIGITAL_FORENSICS",
            "CCTV_VIDEO_FORENSICS",
            "TRACE_EVIDENCE",
            "FOOTWEAR_TIRE_IMPRESSIONS",
            "BALLISTICS_TOOLMARKS",
            "CHAIN_OF_CUSTODY"
        ],
        "dna_evidence": [
            {
                "evidence_id": "EVID-DNA-001",
                "case_id": "DL-2026-0412",
                "sample_id": "SMPL-BIO-DEL-401-A",
                "sample_type": "Touch DNA / Epithelial Swab",
                "biological_material": "Epithelial cellular material with nuclear DNA",
                "collection_location": "Forensic Inspection Bay, PS Kashmere Gate, Delhi",
                "collection_timestamp": "2026-09-03T11:30:00Z",
                "collection_method": "Sterile cotton swab with saline",
                "dna_profile_id": "PROF-STR-DEL-9912",
                "candidate_entity": "person-rakesh",
                "comparison_result": "Consistent Profile / Strong Association",
                "match_confidence": 0.94,
                "laboratory_id": "FSL-ROHINI-BIO",
                "analyst_id": "DR-MEENAKSHI-BIO",
                "report_id": "DNA-FSL-DEL-2026-401",
                "examination_date": "2026-09-04T15:30:00Z",
                "status": "Analyzed / Verified",
                "chain_of_custody_id": "COC-DEL-2026-001",
                "integrity_hash": "a4d8e9c12b7f3a5e8c0d1e2f4a6b8c0e2a4b6d8e0f2a4c6e8b0d2f4a6c8e0b2d",
                "provenance": {"source_system": "FSL Rohini Biology Division", "badge": "FSL-BIO-042"}
            },
            {
                "evidence_id": "EVID-DNA-002",
                "case_id": "DL-2026-0412",
                "sample_id": "SMPL-BIO-DEL-402-B",
                "sample_type": "Hair Follicle with Root Sheath",
                "biological_material": "Human hair root sheath cellular material",
                "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate, Delhi",
                "collection_timestamp": "2026-09-03T11:45:00Z",
                "collection_method": "Fine forceps recovery into sterile glassine envelope",
                "dna_profile_id": "PROF-STR-DEL-9913",
                "candidate_entity": "person-priya",
                "comparison_result": "Investigative Lead / Potential Association",
                "match_confidence": 0.87,
                "laboratory_id": "FSL-ROHINI-BIO",
                "analyst_id": "DR-MEENAKSHI-BIO",
                "report_id": "DNA-FSL-DEL-2026-402",
                "examination_date": "2026-09-04T16:15:00Z",
                "status": "Analyzed / Corroborating Evidence",
                "chain_of_custody_id": "COC-DEL-2026-002",
                "integrity_hash": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3",
                "provenance": {"source_system": "FSL Rohini Biology Division", "badge": "FSL-BIO-042"}
            },
            {
                "evidence_id": "EVID-DNA-003",
                "case_id": "DL-2026-0412",
                "sample_id": "SMPL-BIO-DEL-403-C",
                "sample_type": "Saliva Residue on Paper Filter",
                "biological_material": "Saliva epithelial residue",
                "collection_location": "ISBT Kashmere Gate Departure Gate 2 Verge, Delhi",
                "collection_timestamp": "2026-09-03T09:15:00Z",
                "collection_method": "Clean metal forceps in sterile tamper-evident vial",
                "dna_profile_id": "PROF-STR-DEL-9914",
                "candidate_entity": None,
                "comparison_result": "Inconclusive / Unmatched Third-Party Profile",
                "match_confidence": 0.52,
                "laboratory_id": "FSL-ROHINI-BIO",
                "analyst_id": "DR-MEENAKSHI-BIO",
                "report_id": "DNA-FSL-DEL-2026-403",
                "examination_date": "2026-09-04T17:00:00Z",
                "status": "Requires Human Review / No Known Association",
                "chain_of_custody_id": "COC-DEL-2026-003",
                "integrity_hash": "c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4",
                "provenance": {"source_system": "FSL Rohini Biology Division", "badge": "FSL-BIO-042"}
            }
        ],
        "fingerprint_evidence": [
            {
                "evidence_id": "EVID-FP-001",
                "fingerprint_id": "FP-LAT-DEL-218-A",
                "case_id": "DL-2026-0412",
                "surface_or_object": "Passenger door interior grab handle",
                "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
                "collection_timestamp": "2026-09-03T10:15:00Z",
                "print_quality": "High (14 unambiguous minutiae points)",
                "print_type": "Latent Right Index Fingerprint (Whorl-Loop transition)",
                "candidate_entity": "person-rakesh",
                "similarity_score": 0.91,
                "comparison_result": "Strong Association / AFIS Match",
                "examiner_info": "Inspector K.S. Rathore (Fingerprint Bureau)",
                "report_id": "FP-FSL-DEL-2026-218",
                "status": "Verified / Match Confirmed",
                "chain_of_custody_id": "COC-DEL-2026-004",
                "integrity_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
                "provenance": {"source_system": "Fingerprint Bureau, Crime Branch", "badge": "FPB-EXP-112"}
            },
            {
                "evidence_id": "EVID-FP-002",
                "fingerprint_id": "FP-LAT-DEL-219-B",
                "case_id": "DL-2026-0412",
                "surface_or_object": "Steering wheel rim (9 o'clock position)",
                "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
                "collection_timestamp": "2026-09-03T10:30:00Z",
                "print_quality": "High (15 minutiae points)",
                "print_type": "Latent Left Thumb Print (Plain Arch)",
                "candidate_entity": "person-vikram",
                "similarity_score": 0.94,
                "comparison_result": "Verified Operator Print",
                "examiner_info": "Inspector K.S. Rathore (Fingerprint Bureau)",
                "report_id": "FP-FSL-DEL-2026-219",
                "status": "Verified / Driver Identity Confirmed",
                "chain_of_custody_id": "COC-DEL-2026-005",
                "integrity_hash": "d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8d4e6a8c0",
                "provenance": {"source_system": "Fingerprint Bureau, Crime Branch", "badge": "FPB-EXP-112"}
            },
            {
                "evidence_id": "EVID-FP-003",
                "fingerprint_id": "FP-LAT-DEL-220-C",
                "case_id": "DL-2026-0412",
                "surface_or_object": "Toll receipt paper stub",
                "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
                "collection_timestamp": "2026-09-03T10:45:00Z",
                "print_quality": "Low / Partial Smudge (5 minutiae points)",
                "print_type": "Indeterminate partial friction ridge impression",
                "candidate_entity": "person-rakesh",
                "similarity_score": 0.61,
                "comparison_result": "Inconclusive / Insufficient Minutiae",
                "examiner_info": "Inspector K.S. Rathore (Fingerprint Bureau)",
                "report_id": "FP-FSL-DEL-2026-220",
                "status": "Inconclusive / Requires Secondary Examination",
                "chain_of_custody_id": "COC-DEL-2026-006",
                "integrity_hash": "e6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2",
                "provenance": {"source_system": "Fingerprint Bureau, Crime Branch", "badge": "FPB-EXP-112"}
            }
        ],
        "digital_forensics": [
            {
                "evidence_id": "EVID-DIG-001",
                "device_id": "DEV-SAMSUNG-A52-RAKESH",
                "imei": "358912091823901",
                "sim_identifier": "8991004450192801920",
                "artifact_id": "ART-GPS-GEO-881",
                "artifact_type": "GPS Waypoint & Location Breadcrumb Artifact",
                "application_source": "Google Location History Cache (gservices.db)",
                "recovered_data_type": "Hardware GPS Fix with DOP accuracy 4.2m",
                "timestamp": "2026-09-02T21:40:12Z",
                "location_gps": {"latitude": 28.6675, "longitude": 77.2289, "accuracy_meters": 4.2},
                "associated_phone": "+919871044219",
                "associated_entity": "person-rakesh",
                "extraction_method": "JTAG / Physical Chip Extraction",
                "extraction_date": "2026-09-04T09:30:00Z",
                "forensic_tool": "Cellebrite UFED Physical Analyzer v7.68.2",
                "analyst": "Forensic Scientist Rajesh Chawla",
                "report_id": "DIG-FSL-DEL-2026-309",
                "confidence": 0.94,
                "status": "Corroborating Evidence / Verified Waypoint",
                "integrity_hash": "d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4",
                "provenance": {"source_system": "FSL Rohini Cyber Division", "badge": "FSL-CYB-048"}
            },
            {
                "evidence_id": "EVID-DIG-002",
                "device_id": "DEV-REDMI-NOTE10-VIKRAM",
                "imei": "861942049182301",
                "sim_identifier": "8991004104928172011",
                "artifact_id": "ART-MSG-SIG-402",
                "artifact_type": "Decrypted Instant Message Cache",
                "application_source": "Signal Private Messenger (org.thoughtcrime.securesms)",
                "recovered_data_type": "Deleted encrypted message fragment",
                "timestamp": "2026-09-02T21:52:45Z",
                "associated_phone": "+919711588201",
                "associated_entity": "person-vikram",
                "extraction_method": "Advanced Logical File System Acquisition",
                "extraction_date": "2026-09-04T11:00:00Z",
                "forensic_tool": "MSAB XRY v10.4",
                "analyst": "Forensic Scientist Rajesh Chawla",
                "report_id": "DIG-FSL-DEL-2026-310",
                "confidence": 0.91,
                "status": "Corroborating Evidence / Key Coordination Artifact",
                "integrity_hash": "f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8",
                "provenance": {"source_system": "FSL Rohini Cyber Division", "badge": "FSL-CYB-048"}
            }
        ],
        "cctv_video_forensics": [
            {
                "evidence_id": "EVID-VID-001",
                "cctv_event_id": "VID-EVT-ISBT-GATE2-881",
                "camera_id": "CAM-ISBT-EXT-09",
                "case_id": "DL-2026-0412",
                "timestamp": "2026-09-02T21:42:15Z",
                "location": "ISBT Kashmere Gate Concourse",
                "detected_person": "Male adult, baseball cap, dark jacket",
                "candidate_entity": "person-rakesh",
                "person_similarity_score": 0.81,
                "detected_vehicle": "Maruti Suzuki Swift Dzire, White",
                "vehicle_similarity_score": 0.89,
                "partial_plate": "DL 01 AB **21",
                "frame_reference": "FRM-CAM09-20260902-138402",
                "analyst_or_system": "Forensic Super-Resolution & DeepFace Re-ID",
                "comparison_result": "Investigative Lead / Visual Re-identification Match",
                "confidence": 0.81,
                "report_id": "VID-FSL-DEL-2026-552",
                "integrity_hash": "a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2",
                "provenance": {"source_system": "Video Analytics Cell, FSL Rohini", "badge": "FSL-VID-081"}
            },
            {
                "evidence_id": "EVID-VID-002",
                "cctv_event_id": "VID-EVT-SINGHU-LANE4-102",
                "camera_id": "ANPR-LANE-04",
                "case_id": "DL-2026-0412",
                "timestamp": "2026-09-02T22:15:32Z",
                "location": "Singhu Border Toll Plaza, Lane 4",
                "detected_vehicle": "Maruti Suzuki Swift Dzire, White",
                "vehicle_similarity_score": 0.98,
                "partial_plate": "DL 01 AB 9921",
                "candidate_entity": "vehicle-dl01-9921",
                "frame_reference": "FRM-ANPR04-20260902-881290",
                "analyst_or_system": "Toll ANPR Optical Character Reader",
                "comparison_result": "Confirmed Vehicle Passage / Potential Driver Association",
                "confidence": 0.94,
                "report_id": "VID-FSL-DEL-2026-553",
                "integrity_hash": "b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4",
                "provenance": {"source_system": "Video Analytics Cell, FSL Rohini", "badge": "FSL-VID-081"}
            }
        ],
        "trace_evidence": [
            {
                "evidence_id": "EVID-TRC-001",
                "case_id": "DL-2026-0412",
                "trace_type": "Soil Mineralogy & Particulates",
                "sample_id": "SMPL-SOIL-DEL-114-A",
                "collection_location": "Vehicle Inspection Bay, PS Kashmere Gate",
                "collection_timestamp": "2026-09-03T12:00:00Z",
                "material_characteristics": "Sandy-loam clay enriched with fly-ash microspheres",
                "comparison_candidate": "Singhu Border NH-44 Toll Bypass Unpaved Shoulder Soil",
                "comparison_result": "Strong Association / Geochemical Mineral Concordance",
                "similarity_confidence": 0.88,
                "laboratory": "Chemistry Division, FSL Rohini, Delhi",
                "analyst": "Dr. R.P. Nair",
                "report_id": "TRC-FSL-DEL-2026-114",
                "status": "Corroborating Evidence / Environmental Concordance",
                "chain_of_custody_id": "COC-DEL-2026-007",
                "integrity_hash": "f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0",
                "provenance": {"source_system": "Chemistry Division, FSL Rohini", "badge": "FSL-CHM-053"}
            },
            {
                "evidence_id": "EVID-TRC-002",
                "case_id": "DL-2026-0412",
                "trace_type": "Automotive Paint Transfer Smear",
                "sample_id": "SMPL-PNT-DEL-115-B",
                "collection_location": "Vehicle Left Front Bumper, PS Kashmere Gate",
                "collection_timestamp": "2026-09-03T12:15:00Z",
                "material_characteristics": "Yellow alkyd enamel paint smear over clearcoat",
                "comparison_candidate": "ISBT Kashmere Gate Platform 4 Bollard Paint",
                "comparison_result": "Consistent Multi-Layer Spectral Match",
                "similarity_confidence": 0.87,
                "laboratory": "Physics Division, FSL Rohini, Delhi",
                "analyst": "Sunita Rao",
                "report_id": "TRC-FSL-DEL-2026-115",
                "status": "Corroborating Evidence / Terminal Contact",
                "chain_of_custody_id": "COC-DEL-2026-008",
                "integrity_hash": "a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4",
                "provenance": {"source_system": "Physics Division, FSL Rohini", "badge": "FSL-PHY-029"}
            },
            {
                "evidence_id": "EVID-TRC-003",
                "case_id": "DL-2026-0412",
                "trace_type": "Synthetic Fiber Fragment",
                "sample_id": "SMPL-FBR-DEL-116-C",
                "collection_location": "Front Passenger Headrest, Vehicle DL 01 AB 9921",
                "collection_timestamp": "2026-09-03T12:30:00Z",
                "material_characteristics": "Blue polyester staple fiber",
                "comparison_candidate": "Subject Reported Clothing Reference",
                "comparison_result": "Non-Matching / Exclusionary Fiber (Generic Commercial Upholstery)",
                "similarity_confidence": 0.28,
                "laboratory": "Chemistry Division, FSL Rohini",
                "analyst": "Dr. R.P. Nair",
                "report_id": "TRC-FSL-DEL-2026-116",
                "status": "Exclusionary Finding / Non-Evidentiary",
                "chain_of_custody_id": "COC-DEL-2026-009",
                "integrity_hash": "c4e6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6",
                "provenance": {"source_system": "Chemistry Division, FSL Rohini", "badge": "FSL-CHM-053"}
            }
        ],
        "impression_evidence": [
            {
                "evidence_id": "EVID-IMP-001",
                "impression_id": "IMP-TIRE-DEL-607-A",
                "case_id": "DL-2026-0412",
                "impression_type": "Tire Tread Impression",
                "scene_location": "Muddy Verge beside ISBT Kashmere Gate Departure Gate 2",
                "timestamp": "2026-09-03T09:40:00Z",
                "pattern_characteristics": "4 longitudinal zigzag ribs with variable-pitch tread blocks",
                "size_dimensions": "Tread footprint width 162mm",
                "tread_characteristics": "Bridgestone B290 with localized 4mm circular stone retention cut in groove 2",
                "candidate_vehicle_or_person": "vehicle-dl01-9921",
                "comparison_result": "Strong Match / Individualizing Tread Defect Present",
                "similarity_score": 0.89,
                "confidence": 0.89,
                "analyst": "Inspector M.K. Yadav",
                "report_id": "IMP-FSL-DEL-2026-607",
                "chain_of_custody_id": "COC-DEL-2026-010",
                "integrity_hash": "d6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8",
                "provenance": {"source_system": "Impression Bureau, Crime Branch", "badge": "FPB-IMP-066"}
            },
            {
                "evidence_id": "EVID-IMP-002",
                "impression_id": "IMP-SHOE-DEL-608-B",
                "case_id": "DL-2026-0412",
                "impression_type": "Footwear Outsole Impression",
                "scene_location": "Kerbside verge near passenger boarding point, ISBT Gate 2",
                "timestamp": "2026-09-03T09:50:00Z",
                "pattern_characteristics": "Hexagonal perimeter tread with center chevron pivot",
                "size_dimensions": "Outsole length 294mm (Approx UK Size 9)",
                "tread_characteristics": "Woodland outdoor casual footwear sole with lateral heel erosion",
                "candidate_vehicle_or_person": "person-rakesh",
                "comparison_result": "Investigative Lead / Class Characteristic Concordance",
                "similarity_score": 0.74,
                "confidence": 0.74,
                "analyst": "Inspector M.K. Yadav",
                "report_id": "IMP-FSL-DEL-2026-608",
                "chain_of_custody_id": "COC-DEL-2026-011",
                "integrity_hash": "e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0",
                "provenance": {"source_system": "Impression Bureau, Crime Branch", "badge": "FPB-IMP-066"}
            }
        ],
        "ballistics_toolmarks": [
            {
                "evidence_id": "EVID-BAL-001",
                "case_id": "DL-2026-0412",
                "item_id": "TOOL-PADLOCK-DEL-083-A",
                "evidence_type": "Toolmark Striation Impression",
                "tool_or_weapon_type": "Flat-Blade Steel Pry Lever (tip width 8.5mm)",
                "markings": "Striated scrape lines along brass shackle casing edge",
                "pattern_characteristics": "12 parallel micro-ridges created by tool with chipped corner bevel",
                "recovered_location": "Majnu Ka Tilla Transit Lodge Room 204, Delhi",
                "candidate_tool": "Steel Multi-Tool Pry Lever (Vehicle Boot)",
                "comparison_result": "Potential Match / Microscopic Striation Concordance",
                "similarity_confidence": 0.78,
                "laboratory": "Ballistics & Toolmarks Division, FSL Rohini",
                "analyst": "K.K. Bansal",
                "report_id": "BAL-FSL-DEL-2026-083",
                "chain_of_custody_id": "COC-DEL-2026-012",
                "integrity_hash": "f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2",
                "provenance": {"source_system": "Ballistics Division, FSL Rohini", "badge": "FSL-BAL-017"}
            },
            {
                "evidence_id": "EVID-BAL-002",
                "case_id": "DL-2026-0412",
                "item_id": "TOOL-CHASSIS-DEL-084-B",
                "evidence_type": "Chassis Stamping Verification",
                "tool_or_weapon_type": "Factory Hydraulic Pin-Stamping Machine",
                "markings": "Chassis Plate Stamping: MA3EKB01S0091283",
                "pattern_characteristics": "Factory dot-matrix punch depth strictly conforms to OEM standards",
                "recovered_location": "Engine Firewall, Vehicle DL 01 AB 9921",
                "candidate_tool": "Factory Tooling",
                "comparison_result": "Genuine Factory Stamping / Zero Alteration Detected",
                "similarity_confidence": 0.96,
                "laboratory": "Ballistics & Toolmarks Division, FSL Rohini",
                "analyst": "K.K. Bansal",
                "report_id": "BAL-FSL-DEL-2026-084",
                "chain_of_custody_id": "COC-DEL-2026-013",
                "integrity_hash": "0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b4c6e8f0a2b",
                "provenance": {"source_system": "Ballistics Division, FSL Rohini", "badge": "FSL-BAL-017"}
            }
        ],
        "chain_of_custody": [
            {
                "chain_of_custody_id": "COC-DEL-2026-001",
                "evidence_id": "EVID-DNA-001",
                "case_id": "DL-2026-0412",
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
                        "purpose": "Secure Sealing in Evidence Bag",
                        "custody_status": "SEALED_IN_TRANSIT"
                    },
                    {
                        "transfer_index": 2,
                        "transferred_by": "ASI Balraj Singh",
                        "transferred_by_badge": "DP-MAL-084",
                        "transferred_to": "FSL Rohini Sample Receiving Division",
                        "transferred_to_badge": "DP-COU-302",
                        "transfer_timestamp": "2026-09-03T15:30:00Z",
                        "purpose": "Transfer to Lab for DNA Extraction",
                        "custody_status": "LAB_RECEIVED"
                    },
                    {
                        "transfer_index": 3,
                        "transferred_by": "FSL Reception Clerk",
                        "transferred_by_badge": "FSL-REC-011",
                        "transferred_to": "Dr. Meenakshi Sundaram",
                        "transferred_to_badge": "FSL-BIO-042",
                        "transfer_timestamp": "2026-09-04T09:00:00Z",
                        "purpose": "Forensic STR DNA Profiling",
                        "custody_status": "UNDER_EXAMINATION"
                    },
                    {
                        "transfer_index": 4,
                        "transferred_by": "Dr. Meenakshi Sundaram",
                        "transferred_by_badge": "FSL-BIO-042",
                        "transferred_to": "Central Evidence Storage Vault",
                        "transferred_to_badge": "FSL-MAL-001",
                        "transfer_timestamp": "2026-09-04T18:00:00Z",
                        "purpose": "Cryo-preservation of DNA extract",
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
                "case_id": "DL-2026-0412",
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
                "storage_location": "Locker #402, Fingerprint Bureau, Crime Branch",
                "examination_location": "AFIS Terminal Room, Crime Branch",
                "evidence_status": "ANALYZED_AND_SEALED",
                "original_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
                "current_hash": "c1a9f8b2d4e6a8c0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6e8",
                "hash_algorithm": "SHA-256",
                "integrity_status": "INTACT_VERIFIED",
                "bsa_section_63_compliant": True,
                "report_id": "FP-FSL-DEL-2026-218"
            }
        ]
    }

    # 8. Add Forensic Query Templates
    forensic_queries = [
        {
            "query": "What forensic evidence connects Rakesh Kumar to vehicle DL 01 AB 9921?",
            "answer": "Rakesh Kumar is physically linked to vehicle DL 01 AB 9921 by multiple corroborating forensic findings: (1) Touch DNA epithelial profile matching Rakesh (0.94 confidence) recovered from the passenger seatbelt buckle (DNA-FSL-DEL-2026-401), and (2) Latent fingerprint (FP-LAT-DEL-218-A) matching Rakesh (0.91 similarity) developed on the passenger door grab handle (FP-FSL-DEL-2026-218).",
            "confidence": 0.94,
            "cited_entities": ["person-rakesh", "vehicle-dl01-9921", "evidence-dna-touch-01", "evidence-fp-door-01"],
            "cited_sources": ["DNA-FSL-DEL-2026-401", "FP-FSL-DEL-2026-218", "COC-DEL-2026-001"],
            "suggested_actions": [
                "Inspect passenger seatbelt touch DNA profile in Graph View",
                "Review AFIS fingerprint minutiae matching sheet"
            ]
        },
        {
            "query": "Which physical evidence places vehicle DL 01 AB 9921 at ISBT Kashmere Gate?",
            "answer": "Vehicle DL 01 AB 9921 is placed at ISBT Kashmere Gate by three independent physical corroborations: (1) Tire tread impression at ISBT Gate 2 verge matching right front Bridgestone tire with stone cut defect (0.89 confidence), (2) Left front bumper paint smear spectroscopically matching ISBT Platform 4 yellow bollard paint (0.87 confidence), and (3) CCTV optical sighting and boarding at 21:42 (0.89 confidence).",
            "confidence": 0.91,
            "cited_entities": ["vehicle-dl01-9921", "loc-kashmere-gate", "evidence-tire-isbt-01", "evidence-trace-paint-01", "evidence-vid-isbt-01"],
            "cited_sources": ["IMP-FSL-DEL-2026-607", "TRC-FSL-DEL-2026-115", "VID-FSL-DEL-2026-552"],
            "suggested_actions": [
                "Inspect tire tread defect comparison cast",
                "Review Platform 4 barrier bollard paint FTIR spectrum"
            ]
        },
        {
            "query": "Are there multiple independent forensic corroborations for vehicle movement toward Singhu Border?",
            "answer": "Yes, multiple independent forensic disciplines corroborate the northern route to Singhu Border: (1) High-speed toll ANPR optical plate match at 22:15 (0.94 confidence), (2) Wheel arch soil mineralogy matching Singhu roadside sandy-loam and fly ash profile (0.88 confidence), and (3) Decrypted Signal message from operator Vikram stating 'Heading to Singhu toll' at 21:52 (0.91 confidence).",
            "confidence": 0.93,
            "cited_entities": ["vehicle-dl01-9921", "loc-singhu-border", "evidence-vid-singhu-01", "evidence-trace-soil-01", "evidence-dig-msg-01"],
            "cited_sources": ["ANPR-TOLL-SINGHU-04", "TRC-FSL-DEL-2026-114", "DIG-FSL-DEL-2026-310"],
            "suggested_actions": [
                "View Singhu Border ANPR transit frame",
                "Analyze soil mineralogy concordance report"
            ]
        }
    ]

    existing_queries = {q["query"] for q in data.get("query_templates", [])}
    for q in forensic_queries:
        if q["query"] not in existing_queries:
            data.setdefault("query_templates", []).append(q)

    # 9. Write back with clean formatting
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # 10. Post-expansion validation
    new_nodes_cnt = len(data["graph"]["elements"]["nodes"])
    new_edges_cnt = len(data["graph"]["elements"]["edges"])
    new_entities_cnt = len(data["entities"])
    new_timeline_cnt = len(data["timeline"])
    new_audit_cnt = len(data["provenance"]["audit_trail"])

    print(f"SUCCESS: Expanded to {new_nodes_cnt} nodes (+{new_nodes_cnt - orig_nodes}), {new_edges_cnt} edges (+{new_edges_cnt - orig_edges}), {new_entities_cnt} entities (+{new_entities_cnt - orig_entities}), {new_timeline_cnt} events (+{new_timeline_cnt - orig_timeline}), {new_audit_cnt} audit blocks (+{new_audit_cnt - orig_audit}).")
    print(f"Forensic categories present: {len(data['forensics']['categories_present'])}")

if __name__ == "__main__":
    expand_canonical_case()
