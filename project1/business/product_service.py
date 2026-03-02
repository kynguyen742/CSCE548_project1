from __future__ import annotations
from typing import Optional, List
from db import get_conn
from models import Product


class ProductService:
    def list_products(self, limit: int = 20, vendor_id: int | None = None) -> List[Product]:
        q = "SELECT product_id, vendor_id, name, version, platform FROM products"
        params = []
        if vendor_id is not None:
            q += " WHERE vendor_id=%s"
            params.append(vendor_id)
        q += " ORDER BY product_id DESC LIMIT %s"
        params.append(limit)

        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(q, tuple(params))
            rows = cur.fetchall()
            return [Product(**r) for r in rows]

    def get_product(self, product_id: int) -> Optional[Product]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT product_id, vendor_id, name, version, platform FROM products WHERE product_id=%s",
                (product_id,),
            )
            r = cur.fetchone()
            return Product(**r) if r else None

    def create_product(self, p: Product) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (vendor_id, name, version, platform) VALUES (%s, %s, %s, %s)",
                (p.vendor_id, p.name, p.version, p.platform),
            )
            conn.commit()
            return int(cur.lastrowid)

    def update_product(self, product_id: int, vendor_id: int, name: str, version: str | None, platform: str | None) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET vendor_id=%s, name=%s, version=%s, platform=%s WHERE product_id=%s",
                (vendor_id, name, version, platform, product_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
            conn.commit()
            return cur.rowcount > 0