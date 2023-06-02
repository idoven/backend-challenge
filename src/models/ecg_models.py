from pydantic import BaseModel, conlist
from datetime import datetime


class ECGLead(BaseModel):
    name: str
    samples: int = -1
    signal: list[int]


class ECGData(BaseModel):
    id: int
    date: datetime
    leads: conlist(ECGLead, min_items=0)


class ECGLeadResult(BaseModel):
    name: str
    zero_passes: int = 0
    # Add more useful results


class ECGResults(BaseModel):
    id: int
    date: datetime
    lead_results: conlist(ECGLeadResult, min_items=0)
    # Add more items involving multiple leads (e.g. anomalies_found)
