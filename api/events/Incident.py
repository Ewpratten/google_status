from dataclasses import dataclass
from typing import Optional
import datetime


@dataclass
class Incident:

    # Time
    time_start: datetime.datetime

    # Info
    description: str
    service: str
    severity: str
    
    # Optionals    
    time_end: Optional[datetime.datetime] = None
    url: Optional[str] = None
