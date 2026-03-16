from __future__ import annotations
from flask import Blueprint, jsonify, request
from business.vendor_service import VendorService
from models import Vendor

bp = Blueprint("vendors", __name__)
service = VendorService()

def vendor_to_dict(v: Vendor) -> dict:
    return {"vendor_id": v.vendor_id, "name": v.name, "website": v.website}

@bp.get("/vendors")
def list_vendors():
    limit = int(request.args.get("limit", 20))
    name = request.args.get("name")
    rows = service.search_by_name(name, limit) if name else service.list_vendors(limit)
    return jsonify([vendor_to_dict(v) for v in rows]), 200

@bp.get("/vendors/<int:vendor_id>")
def get_vendor(vendor_id: int):
    v = service.get_vendor(vendor_id)
    if not v:
        return jsonify({"error": "Not found"}), 404
    return jsonify(vendor_to_dict(v)), 200

@bp.post("/vendors")
def create_vendor():
    data = request.get_json(force=True)
    try:
        v = Vendor(vendor_id=None, name=str(data["name"]), website=data.get("website"))
        new_id = service.create_vendor(v)
        return jsonify({"vendor_id": new_id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@bp.put("/vendors/<int:vendor_id>")
def update_vendor(vendor_id: int):
    data = request.get_json(force=True)
    try:
        ok = service.update_vendor(vendor_id, str(data["name"]), data.get("website"))
        if not ok:
            return jsonify({"error": "Not found / no change"}), 404
        return jsonify({"updated": True}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@bp.delete("/vendors/<int:vendor_id>")
def delete_vendor(vendor_id: int):
    ok = service.delete_vendor(vendor_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200