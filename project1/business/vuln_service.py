# src/business/vuln_service.py
from __future__ import annotations

from datetime import date
from typing import List, Optional

from models import Vulnerability
from vuln_dao import VulnerabilityDAO


class VulnerabilityService:
    """
    Business layer. Sits between DAO and API.

    Business rules included:
    - Normalize severity/status to uppercase
    - Validate allowed severity/status
    - Validate CVSS range
    - Validate CVE format prefix
    """

    ALLOWED_SEVERITY = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    ALLOWED_STATUS = {"OPEN", "PATCHED", "MITIGATED"}

    def __init__(self, dao: VulnerabilityDAO | None = None):
        self.dao = dao or VulnerabilityDAO()

    # CREATE
    def create_vulnerability(self, v: Vulnerability) -> int:
        v = self._normalize(v)
        self._validate(v)
        return self.dao.create(v)

    # READ (one)
    def get_vulnerability(self, vuln_id: int) -> Optional[Vulnerability]:
        return self.dao.get_by_id(vuln_id)

    # READ (many)
    def list_vulnerabilities(self, limit: int = 20) -> List[Vulnerability]:
        return self.dao.list_all(limit)

    def search_by_severity(self, severity: str, limit: int = 20) -> List[Vulnerability]:
        sev = (severity or "").strip().upper()
        if sev not in self.ALLOWED_SEVERITY:
            raise ValueError(f"Invalid severity '{severity}'. Must be one of {sorted(self.ALLOWED_SEVERITY)}")
        return self.dao.search_by_severity(sev, limit)

    # UPDATE
    def update_status(self, vuln_id: int, new_status: str) -> bool:
        status = (new_status or "").strip().upper()
        if status not in self.ALLOWED_STATUS:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {sorted(self.ALLOWED_STATUS)}")
        return self.dao.update_status(vuln_id, status)

    # DELETE
    def delete_vulnerability(self, vuln_id: int) -> bool:
        return self.dao.delete(vuln_id)

    # -------- helpers --------
    def _normalize(self, v: Vulnerability) -> Vulnerability:
        return Vulnerability(
            vuln_id=v.vuln_id,
            product_id=v.product_id,
            cve_id=(v.cve_id or "").strip().upper(),
            title=(v.title or "").strip(),
            description=(v.description or "").strip(),
            severity=(v.severity or "").strip().upper(),
            cvss=float(v.cvss),
            published_date=v.published_date if isinstance(v.published_date, date) else date.fromisoformat(str(v.published_date)),
            status=(v.status or "").strip().upper(),
        )

    def _validate(self, v: Vulnerability) -> None:
        if not v.cve_id.startswith("CVE-"):
            raise ValueError("cve_id must start with 'CVE-'")
        if v.severity not in self.ALLOWED_SEVERITY:
            raise ValueError(f"severity must be one of {sorted(self.ALLOWED_SEVERITY)}")
        if v.status not in self.ALLOWED_STATUS:
            raise ValueError(f"status must be one of {sorted(self.ALLOWED_STATUS)}")
        if not (0.0 <= v.cvss <= 10.0):
            raise ValueError("cvss must be between 0.0 and 10.0")
        if v.product_id <= 0:
            raise ValueError("product_id must be a positive integer")