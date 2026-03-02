from __future__ import annotations
from typing import Optional, List
from db import get_conn
from models import VulnerabilityReference


class ReferenceService:
    def list_references(self, limit: int = 20, vuln_id: int | None = None) -> List[VulnerabilityReference]:
        q = "SELECT ref_id, vuln_id, ref_type, url, note FROM vuln_references"
        params = []
        if vuln_id is not None:
            q += " WHERE vuln_id=%s"
            params.append(vuln_id)
        q += " ORDER BY ref_id DESC LIMIT %s"
        params.append(limit)

        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(q, tuple(params))
            rows = cur.fetchall()
            return [VulnerabilityReference(**r) for r in rows]

    def get_reference(self, ref_id: int) -> Optional[VulnerabilityReference]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT ref_id, vuln_id, ref_type, url, note FROM vuln_references WHERE ref_id=%s", (ref_id,))
            r = cur.fetchone()
            return VulnerabilityReference(**r) if r else None

    def create_reference(self, r: VulnerabilityReference) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO vuln_references (vuln_id, ref_type, url, note) VALUES (%s, %s, %s, %s)",
                (r.vuln_id, r.ref_type, r.url, r.note),
            )
            conn.commit()
            return int(cur.lastrowid)

    def update_reference(self, ref_id: int, ref_type: str, url: str, note: str | None) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE vuln_references SET ref_type=%s, url=%s, note=%s WHERE ref_id=%s",
                (ref_type, url, note, ref_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_reference(self, ref_id: int) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM vuln_references WHERE ref_id=%s", (ref_id,))
            conn.commit()
            return cur.rowcount > 0