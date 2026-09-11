"""
Master Synthetic Data Generator for KavachNet (SIH 2026, PS #26189)
Generates multi-source synthetic logs across all 6 investigative sources:
1. FIR Records (data/raw/firs/)
2. Call Detail Records (CDRs) (data/raw/cdrs/)
3. Banking & UPI Records (data/raw/banking/)
4. CCTV & ANPR Sighting Logs (data/raw/cctv/)
5. Hotel & Lodge Registers (data/raw/hotels/)
6. Forensic & Cyber Reports (data/raw/forensics/)
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from data.generators.generate_firs import generate_firs
from data.generators.generate_cdrs import generate_cdrs
from data.generators.generate_banking import generate_banking
from data.generators.generate_cctv_anpr import generate_cctv_anpr
from data.generators.generate_hotels import generate_hotels
from data.generators.generate_forensics import generate_forensics

def generate_all_sources():
    print("=" * 65)
    print("  KavachNet — Generating Multi-Source Synthetic Case Records  ")
    print("=" * 65)
    
    firs = generate_firs()
    cdrs = generate_cdrs()
    banking = generate_banking()
    cctv = generate_cctv_anpr()
    hotels = generate_hotels()
    forensics = generate_forensics()

    total = len(firs) + len(cdrs) + len(banking) + len(cctv) + len(hotels) + len(forensics)
    print("=" * 65)
    print(f"  SUCCESS: Generated {total} multi-source evidentiary records  ")
    print("=" * 65)
    return {
        "firs": len(firs),
        "cdrs": len(cdrs),
        "banking": len(banking),
        "cctv": len(cctv),
        "hotels": len(hotels),
        "forensics": len(forensics),
        "total": total
    }

if __name__ == "__main__":
    generate_all_sources()
