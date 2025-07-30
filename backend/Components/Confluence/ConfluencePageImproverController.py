from flask import Blueprint, request, jsonify
from ConfluencePageImproverHelper import improve_confluence_page

confluence_page_improver_bp = Blueprint("confluence_page_improver", __name__)

@confluence_page_improver_bp.route("/confluence/improve_page", methods=["POST"])
def improve_page():
    data = request.get_json()
    page_id = data.get("page_id")

    if not page_id:
        return jsonify({"success": False, "error": "Missing page_id"}), 400

    result = improve_confluence_page(page_id)
    return jsonify(result), 200 if result.get("success") else 500
