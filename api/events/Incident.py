from dataclasses import dataclass
from typing import Optional


@dataclass
class Incident:

    # Time
    time_start: str
    time_end: Optional[str] = None

    # Info
    description: str
    service: str
    severity: str
    
    # External
    url: Optional[str] = None
