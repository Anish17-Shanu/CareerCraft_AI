from flask import Blueprint, jsonify, request
from services.external_suggestions import fetch_external_bundle

external_bp = Blueprint("external", __name__)


@external_bp.route("/external/suggest")
def external_suggest():
    query = request.args.get("q", "").strip()
    bundle = fetch_external_bundle(query)
    return jsonify({"query": query, **bundle})
