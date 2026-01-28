from typing import List, Optional
from db import get_connection
from models import Vulnerability

class VulnerabilityDAO:
    # CREATE
    def create(self, v: Vulnerability) -> int:
        sql = """
        INSERT INTO vulnerabilities (product_id, cve_id, title, description, severity, cvss, published_date, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (v.product_id, v.cve_id, v.title, v.description, v.severity, v.cvss, v.published_date, v.status))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    # READ (one)
    def get_by_id(self, vuln_id: int) -> Optional[Vulnerability]:
        sql = "SELECT vuln_id, product_id, cve_id, title, description, severity, cvss, published_date, status FROM vulnerabilities WHERE vuln_id=%s"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (vuln_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        return Vulnerability(*row)

    # READ (many)
    def list_all(self, limit: int = 20) -> List[Vulnerability]:
        sql = """
        SELECT vuln_id, product_id, cve_id, title, description, severity, cvss, published_date, status
        FROM vulnerabilities
        ORDER BY published_date DESC
        LIMIT %s
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Vulnerability(*r) for r in rows]

    def search_by_severity(self, severity: str, limit: int = 20) -> List[Vulnerability]:
        sql = """
        SELECT vuln_id, product_id, cve_id, title, description, severity, cvss, published_date, status
        FROM vulnerabilities
        WHERE severity=%s
        ORDER BY published_date DESC
        LIMIT %s
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (severity, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Vulnerability(*r) for r in rows]

    # UPDATE
    def update_status(self, vuln_id: int, new_status: str) -> bool:
        sql = "UPDATE vulnerabilities SET status=%s WHERE vuln_id=%s"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (new_status, vuln_id))
        conn.commit()
        changed = (cur.rowcount > 0)
        cur.close()
        conn.close()
        return changed

    # DELETE
    def delete(self, vuln_id: int) -> bool:
        sql = "DELETE FROM vulnerabilities WHERE vuln_id=%s"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (vuln_id,))
        conn.commit()
        deleted = (cur.rowcount > 0)
        cur.close()
        conn.close()
        return deleted
