from __future__ import annotations
from flask import Blueprint, jsonify, request
from business.product_service import ProductService
from models import Product

bp = Blueprint("products", __name__)
service = ProductService()

def product_to_dict(p: Product) -> dict:
    return {
        "product_id": p.product_id,
        "vendor_id": p.vendor_id,
        "name": p.name,
        "version": p.version,
        "platform": p.platform,
    }

@bp.get("/products")
def list_products():
    limit = int(request.args.get("limit", 20))
    vendor_id = request.args.get("vendor_id")
    rows = service.list_products(limit=limit, vendor_id=int(vendor_id) if vendor_id else None)
    return jsonify([product_to_dict(p) for p in rows]), 200

@bp.get("/products/<int:product_id>")
def get_product(product_id: int):
    p = service.get_product(product_id)
    if not p:
        return jsonify({"error": "Not found"}), 404
    return jsonify(product_to_dict(p)), 200

@bp.post("/products")
def create_product():
    data = request.get_json(force=True)
    try:
        p = Product(
            product_id=None,
            vendor_id=int(data["vendor_id"]),
            name=str(data["name"]),
            version=data.get("version"),
            platform=data.get("platform"),
        )
        new_id = service.create_product(p)
        return jsonify({"product_id": new_id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.put("/products/<int:product_id>")
def update_product(product_id: int):
    data = request.get_json(force=True)
    try:
        ok = service.update_product(
            product_id=product_id,
            vendor_id=int(data["vendor_id"]),
            name=str(data["name"]),
            version=data.get("version"),
            platform=data.get("platform"),
        )
        if not ok:
            return jsonify({"error": "Not found / no change"}), 404
        return jsonify({"updated": True}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.delete("/products/<int:product_id>")
def delete_product(product_id: int):
    ok = service.delete_product(product_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": True}), 200