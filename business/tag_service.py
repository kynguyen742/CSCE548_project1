from __future__ import annotations
from typing import Optional, List
from db import get_conn
from models import Tag


class TagService:
    def list_tags(self, limit: int = 50) -> List[Tag]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT tag_id, name FROM tags ORDER BY tag_id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            return [Tag(**r) for r in rows]

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT tag_id, name FROM tags WHERE tag_id=%s", (tag_id,))
            r = cur.fetchone()
            return Tag(**r) if r else None

    def search_by_name(self, name: str, limit: int = 50) -> List[Tag]:
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT tag_id, name FROM tags WHERE name LIKE %s ORDER BY tag_id DESC LIMIT %s", (f"%{name}%", limit))
            rows = cur.fetchall()
            return [Tag(**r) for r in rows]

    def create_tag(self, t: Tag) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO tags (name) VALUES (%s)", (t.name,))
            conn.commit()
            return int(cur.lastrowid)

    def delete_tag(self, tag_id: int) -> bool:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM tags WHERE tag_id=%s", (tag_id,))
            conn.commit()
            return cur.rowcount > 0