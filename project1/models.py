from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Vulnerability:
    vuln_id: Optional[int]
    product_id: int
    cve_id: str
    title: str
    description: str
    severity: str
    cvss: float
    published_date: date
    status: str
