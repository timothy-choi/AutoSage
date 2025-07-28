from flask import Blueprint, request, jsonify
from ConfluenceToNotionSyncerHelper import sync_confluence_to_notion

confluence_to_notion_syncer_bp = Blueprint("confluence_to_notion_syncer", __name__)

@confluence_to_notion_syncer_bp.route("/confluence/to_notion", methods=["POST"])
def confluence_to_notion():
    data = request.get_json()
    if "confluence_page_id" not in data or "notion_database_id" not in data:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    result = sync_confluence_to_notion(data["confluence_page_id"], data["notion_database_id"])
    return jsonify(result), 200 if result.get("success") else 500
