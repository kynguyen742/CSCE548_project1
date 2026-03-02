from __future__ import annotations
from typing import Optional, List
from db import get_conn
from models import Vendor


class VendorService:
    def list_vendors(self, limit: int = 20) -> List[Vendor]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT vendor_id, name, website FROM vendors ORDER BY vendor_id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            return [Vendor(**r) for r in rows]

    def get_vendor(self, vendor_id: int) -> Optional[Vendor]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT vendor_id, name, website FROM vendors WHERE vendor_id=%s", (vendor_id,))
            r = cur.fetchone()
            return Vendor(**r) if r else None

    def search_by_name(self, name: str, limit: int = 20) -> List[Vendor]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT vendor_id, name, website FROM vendors WHERE name LIKE %s ORDER BY vendor_id DESC LIMIT %s",
                (f"%{name}%", limit),
            )
            rows = cur.fetchall()
            return [Vendor(**r) for r in rows]

    def create_vendor(self, v: Vendor) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO vendors (name, website) VALUES (%s, %s)", (v.name, v.website))
            conn.commit()
            return int(cur.lastrowid)

    def update_vendor(self, vendor_id: int, name: str, website: str | None) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE vendors SET name=%s, website=%s WHERE vendor_id=%s", (name, website, vendor_id))
            conn.commit()
            return cur.rowcount > 0

    def delete_vendor(self, vendor_id: int) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM vendors WHERE vendor_id=%s", (vendor_id,))
            conn.commit()
            return cur.rowcount > 0