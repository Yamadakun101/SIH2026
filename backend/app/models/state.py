from pydantic import BaseModel

class StateItem(BaseModel):
    state_code: str
    state_name: str
    active_cases_count: int
    high_risk_alerts: int
    lat: float
    lng: float
