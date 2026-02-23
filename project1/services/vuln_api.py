# src/services/vuln_api.py
"""
How to run (local dev):
1) pip install -r requirements.txt
2) Set DB_* environment variables (see README)
3) From project2/ run:
   python -m src.services.vuln_api

Then API will run at:
  http://127.0.0.1:5000

Endpoints:
  GET    /health
  GET    /vulnerabilities?limit=10
  GET    /vulnerabilities/<id>
  GET    /vulnerabilities/search?severity=HIGH&limit=10
  POST   /vulnerabilities
  PATCH  /vulnerabilities/<id>/status
  DELETE /vulnerabilities/<id>
"""

from __future__ import annotations

from datetime import date
from flask import Flask, jsonify, request

from business.vuln_service import VulnerabilityService
from models import Vulnerability


app = Flask(__name__)
service = VulnerabilityService()


def vuln_to_dict(v: Vulnerability) -> dict:
    return {
        "vuln_id": v.vuln_id,
        "product_id": v.product_id,
        "cve_id": v.cve_id,
        "title": v.title,
        "description": v.description,
        "severity": v.severity,
        "cvss": v.cvss,
        "published_date": v.published_date.isoformat() if hasattr(v.published_date, "isoformat") else str(v.published_date),
        "status": v.status,
    }


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/vulnerabilities")
def list_vulns():
    limit = int(request.args.get("limit", 20))
    vulns = service.list_vulnerabilities(limit)
    return jsonify([vuln_to_dict(v) for v in vulns]), 200


@app.get("/vulnerabilities/<int:vuln_id>")
def get_vuln(vuln_id: int):
    v = service.get_vulnerability(vuln_id)
    if not v:
        return jsonify({"error": "Not found"}), 404
    return jsonify(vuln_to_dict(v)), 200


@app.get("/vulnerabilities/search")
def search_by_severity():
    severity = request.args.get("severity", "")
    limit = int(request.args.get("limit", 20))
    try:
        vulns = service.search_by_severity(severity, limit)
        return jsonify([vuln_to_dict(v) for v in vulns]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.post("/vulnerabilities")
def create_vuln():
    data = request.get_json(force=True)

    try:
        v = Vulnerability(
            vuln_id=None,
            product_id=int(data["product_id"]),
            cve_id=str(data["cve_id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            severity=str(data["severity"]),
            cvss=float(data["cvss"]),
            published_date=date.fromisoformat(str(data["published_date"])),
            status=str(data["status"]),
        )
        new_id = service.create_vulnerability(v)
        return jsonify({"vuln_id": new_id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.patch("/vulnerabilities/<int:vuln_id>/status")
def update_status(vuln_id: int):
    data = request.get_json(force=True)
    try:
        new_status = str(data["status"])
        ok = service.update_status(vuln_id, new_status)
        if not ok:
            return jsonify({"error": "Not found / no change"}), 404
        return jsonify({"updated": True}), 200
    except KeyError:
        return jsonify({"error": "Missing field: status"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.delete("/vulnerabilities/<int:vuln_id>")
def delete_vuln(vuln_id: int):
    ok = service.delete_vulnerability(vuln_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200


if __name__ == "__main__":
    # For production hosting:
    # - Use gunicorn (Linux/Mac) or waitress (Windows) instead of Flask dev server.
    # Example (Windows recommended):
    #   pip install waitress
    #   waitress-serve --listen=127.0.0.1:5000 src.services.vuln_api:app
    app.run(host="127.0.0.1", port=5000, debug=True)