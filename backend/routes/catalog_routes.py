from flask import Blueprint, jsonify
from services.catalog_service import get_catalog

catalog_bp = Blueprint("catalog", __name__)

@catalog_bp.route("/catalog")
def catalog():
    return jsonify(get_catalog())
