from __future__ import annotations
from flask import Blueprint, jsonify, request
from business.reference_service import ReferenceService
from models import VulnerabilityReference

bp = Blueprint("references", __name__)
service = ReferenceService()

def ref_to_dict(r: VulnerabilityReference) -> dict:
    return {"ref_id": r.ref_id, "vuln_id": r.vuln_id, "ref_type": r.ref_type, "url": r.url, "note": r.note}

@bp.get("/references")
def list_refs():
    limit = int(request.args.get("limit", 20))
    vuln_id = request.args.get("vuln_id")
    rows = service.list_references(limit=limit, vuln_id=int(vuln_id) if vuln_id else None)
    return jsonify([ref_to_dict(r) for r in rows]), 200

@bp.get("/references/<int:ref_id>")
def get_ref(ref_id: int):
    r = service.get_reference(ref_id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ref_to_dict(r)), 200

@bp.post("/references")
def create_ref():
    data = request.get_json(force=True)
    try:
        r = VulnerabilityReference(
            ref_id=None,
            vuln_id=int(data["vuln_id"]),
            ref_type=str(data["ref_type"]),
            url=str(data["url"]),
            note=data.get("note"),
        )
        new_id = service.create_reference(r)
        return jsonify({"ref_id": new_id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.put("/references/<int:ref_id>")
def update_ref(ref_id: int):
    data = request.get_json(force=True)
    try:
        ok = service.update_reference(ref_id, str(data["ref_type"]), str(data["url"]), data.get("note"))
        if not ok:
            return jsonify({"error": "Not found / no change"}), 404
        return jsonify({"updated": True}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@bp.delete("/references/<int:ref_id>")
def delete_ref(ref_id: int):
    ok = service.delete_reference(ref_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200