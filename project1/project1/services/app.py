from __future__ import annotations
from flask import Flask, jsonify
from flask_cors import CORS


from .vuln_api import bp as vuln_bp
from .vendor_api import bp as vendor_bp
from .product_api import bp as product_bp
from .reference_api import bp as ref_bp
from .tag_api import bp as tag_bp
from .vulnerability_tag_api import bp as vt_bp


def create_app() -> Flask:
    app = Flask(__name__)

    CORS(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    app.register_blueprint(vuln_bp)
    app.register_blueprint(vendor_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(ref_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(vt_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)