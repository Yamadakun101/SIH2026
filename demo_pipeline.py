"""
KavachNet End-to-End Pipeline Demonstration
Problem Statement #26189 — AI-Powered Criminal Network Analysis System
Ministry of Home Affairs → NCRB / Women Safety Division
Legal Compliance: Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63
"""

import json
import sys
import time
from pathlib import Path

# Ensure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.assistant_engine import InvestigativeAssistantEngine
from ai.entity_resolution import EntityResolver
from ai.ner_extractor import MultiSourceNERExtractor
from blockchain.bsa_certificate import BSACertificateGenerator
from blockchain.custody_ledger import EvidenceCustodyLedger
from blockchain.hash_chain import EvidenceHashChain
from graph.centrality_analytics import CentralityAnalytics
from graph.graph_builder import CrimeGraph
from graph.syndicate_clustering import SyndicateClustering


def print_banner():
    banner = r"""
================================================================================
   _  __                     __    _   __     __ 
  / |/ /__ __  _____ _____ _/ /_  / | / /__  / /_
 /    / _ `/ |/ / _ `/ __// __ \/  |/ / -_)/ __/
/_/|_/\_,_/|___/\_,_/\__//_/ /_/_/ |_/\__/ \__/  
================================================================================
 AI-POWERED CRIMINAL NETWORK ANALYSIS & PROVENANCE SYSTEM | SIH 2026 (PS #26189)
 Legal Framework: Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63
 Lead Agency: Special Cell / Crime Branch, Delhi Police
================================================================================
"""
    print(banner)


def run_pipeline():
    print_banner()

    # Step 1: Load Canonical Case
    case_path = ROOT_DIR / "data" / "dl-2026-0412.json"
    print(f"\n[*] [STAGE 1] INGESTING CANONICAL CASE RECORD: {case_path.name}")
    with open(case_path, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    meta = case_data["case_metadata"]
    print(f"    Case ID:          {meta['case_id']}")
    print(f"    Incident Date:    {meta['incident_date']}")
    print(f"    Title:            {meta['title']}")
    print(f"    Lead Agency:      {meta['lead_agency']}")
    print(f"    FIR Reference:    {meta['fir_number']}")
    print(f"    Initial Status:   {meta['status']} (Priority: {meta['priority']})")

    # Step 2: Multi-Source NER Extraction & Entity Resolution
    print("\n[*] [STAGE 2] EXECUTING MULTI-SOURCE NER & ENTITY DEDUPLICATION")
    sample_fir_text = (
        "Complainant stated that Priya Sharma (age 22) was last seen at ISBT Kashmere Gate around 21:30. "
        "Cell phone +91 98112 00341 went silent at 21:45. Multiple incoming calls from burner SIM 98710-44219. "
        "Suspect vehicle White Swift Dzire (DL 01 AB 9921) sighted moving north towards Singhu Border Toll Plaza."
    )
    extractor = MultiSourceNERExtractor()
    extracted = extractor.extract_all(sample_fir_text, source_context="FIR_STATEMENT")
    print(f"    Extracted {len(extracted)} entities from raw text stream:")
    for ent in extracted:
        print(f"      - [{ent.entity_type:12s}] {ent.raw_text:24s} -> {ent.normalized_value:22s} (Confidence: {ent.confidence:.0%})")

    resolver = EntityResolver()
    norm_phone = resolver.normalize_phone("+91-98710-44219")
    norm_vehicle = resolver.normalize_vehicle("dl 01 ab 9921")
    print(f"    Entity Normalization -> Phone: {norm_phone} | Plate: {norm_vehicle}")

    # Step 3: Knowledge Graph Construction & Centrality Metrics
    print("\n[*] [STAGE 3] BUILDING KNOWLEDGE GRAPH & COMPUTING CENTRALITY SCORES")
    graph = CrimeGraph.from_case_json(case_data)
    print(f"    Graph compiled: {len(graph.nodes)} Nodes, {len(graph.edges)} Edges.")

    centrality = CentralityAnalytics(graph)
    centrality.apply_centrality_to_graph()
    top_hubs = centrality.get_top_hub_entities(top_k=3)

    print("    Top Facilitator / High Centrality Nodes Identified:")
    for rank, hub in enumerate(top_hubs, 1):
        print(
            f"      {rank}. {hub['label']} ({hub['type']}) "
            f"| Composite Score: {hub['composite_centrality_score']} "
            f"| Betweenness: {hub['betweenness_centrality']} "
            f"-> [{hub['investigative_observation']}]"
        )

    # Step 4: Syndicate Community Clustering & Suspicious Path Tracing
    print("\n[*] [STAGE 4] SYNDICATE COMMUNITY DETECTION & MULTI-HOP PATHFINDING")
    clustering = SyndicateClustering(graph)
    clusters = clustering.get_clusters_summary()
    print(f"    Detected {len(clusters)} isolated syndicates / operational sub-clusters:")
    for c in clusters:
        member_names = ", ".join([m["label"] for m in c["members"][:3]])
        print(f"      - {c['cluster_name']} (Size: {c['size']}) -> Members: {member_names}...")

    path_steps = clustering.find_shortest_path("person-rakesh", "loc-singhu-border")
    if path_steps:
        path_labels = [step["node"]["label"] for step in path_steps]
        print(f"    Suspicious Flow Path (Suspect -> Vehicle Corridor):")
        print("      " + " -> ".join(path_labels))

    # Step 5: BSA 2023 Section 63 Cryptographic Evidence Ledger & Certificate
    print("\n[*] [STAGE 5] GENERATING BSA 2023 SEC 63 DIGITAL EVIDENCE CERTIFICATE")
    ledger = EvidenceCustodyLedger(case_id=meta["case_id"])
    ledger.populate_from_case_dataset(case_data=case_data, officer_badge="DP-SI-4921")
    
    verification = ledger.get_verification_payload()
    print(f"    Chain Verification:   {'[PASS] VERIFIED INTACT' if verification['bsa_section_63_compliant'] else '[FAIL] CORRUPTED'}")
    print(f"    Merkle Root Hash:     {verification['merkle_root']}")
    print(f"    Total Logged Blocks:  {verification['total_evidence_blocks']}")

    cert_gen = BSACertificateGenerator(ledger=ledger)
    certificate = cert_gen.generate_certificate(
        certifying_officer_name="Inspector Rajesh Meena",
        certifying_officer_badge="DP-INSP-8821",
        police_station_agency=meta["lead_agency"]
    )
    print(f"    Certificate ID:       {certificate['certificate_id']}")
    print(f"    Legal Statute:        {certificate['statutory_provision']}")
    print(f"    Admissibility Status: {'LEGALLY VALID & ADMISSIBLE' if certificate['status'] == 'VALID' else 'INVALID'}")

    # Step 6: AI Investigative Assistant Q&A
    print("\n[*] [STAGE 6] AI INVESTIGATIVE ASSISTANT (CONVERSATIONAL INFERENCE)")
    assistant = InvestigativeAssistantEngine(case_data=case_data, graph=graph)

    sample_questions = [
        "What connects Rakesh Kumar to the vehicle sighted at Singhu Border?",
        "Who was in contact with Priya Sharma before her mobile signal went dead?",
        "Identify any mule bank accounts and rapid financial withdrawals."
    ]

    for q in sample_questions:
        print(f"\n    Q: \"{q}\"")
        ans = assistant.answer_query(q)
        print(f"    A: {ans['answer']}")
        print(f"       [Confidence: {ans['confidence']:.0%}] | Citations: {', '.join(ans['cited_entities'])}")
        print(f"       Suggested Action: {ans['suggested_actions'][0]}")

    print("\n" + "=" * 80)
    print(" [✓] PIPELINE EXECUTION COMPLETE: ALL 6 STAGES OPERATIONAL & VERIFIED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_pipeline()
