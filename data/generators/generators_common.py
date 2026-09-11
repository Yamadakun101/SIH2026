from pathlib import Path
from faker import Faker

fake = Faker("en_IN")
Faker.seed(2026)

BASE_DATA_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DATA_DIR / "raw"

# Create target subdirectories
FIRS_DIR = RAW_DIR / "firs"
CDRS_DIR = RAW_DIR / "cdrs"
BANKING_DIR = RAW_DIR / "banking"
CCTV_DIR = RAW_DIR / "cctv"
HOTELS_DIR = RAW_DIR / "hotels"
FORENSICS_DIR = RAW_DIR / "forensics"

for d in [FIRS_DIR, CDRS_DIR, BANKING_DIR, CCTV_DIR, HOTELS_DIR, FORENSICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Canonical Case DL-2026-0412 Constants
CASE_ID = "DL-2026-0412"
PRIYA_PHONE = "+919811200341"
PRIYA_IMEI = "864201049281720"
RAKESH_PHONE = "+919871044219"
RAKESH_IMEI = "358912091823901"
VIKRAM_PHONE = "+919711588201"
VIKRAM_VEHICLE = "DL 01 AB 9921"
TOWER_KASHMERE = "TOW-DEL-KASHMERE-482"
TOWER_SINGHU = "TOW-DEL-SINGHU-109"
ATM_CIVIL_LINES = "ATM-DEL-CIVIL-04"
ANPR_SINGHU = "ANPR-LANE-04"
MULE_ACCOUNT = "HDFC-••4091"
MULE_VPA = "rkenterprises@okhdfc"
