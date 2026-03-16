from __future__ import annotations
from flask import Blueprint, jsonify, request
from business.tag_service import TagService
from models import Tag

bp = Blueprint("tags", __name__)
service = TagService()

def tag_to_dict(t: Tag) -> dict:
    return {"tag_id": t.tag_id, "name": t.name}

@bp.get("/tags")
def list_tags():
    limit = int(request.args.get("limit", 50))
    name = request.args.get("name")
    rows = service.search_by_name(name, limit) if name else service.list_tags(limit)
    return jsonify([tag_to_dict(t) for t in rows]), 200

@bp.get("/tags/<int:tag_id>")
def get_tag(tag_id: int):
    t = service.get_tag(tag_id)
    if not t:
        return jsonify({"error": "Not found"}), 404
    return jsonify(tag_to_dict(t)), 200

@bp.post("/tags")
def create_tag():
    data = request.get_json(force=True)
    try:
        t = Tag(tag_id=None, name=str(data["name"]))
        new_id = service.create_tag(t)
        return jsonify({"tag_id": new_id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@bp.delete("/tags/<int:tag_id>")
def delete_tag(tag_id: int):
    ok = service.delete_tag(tag_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200