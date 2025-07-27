from flask import Blueprint, request, jsonify
from ConfluenceToSlackBridgeHelper import bridge_confluence_to_slack

confluence_to_slack_bridge_bp = Blueprint("confluence_to_slack_bridge", __name__)

@confluence_to_slack_bridge_bp.route("/confluence/to_slack", methods=["POST"])
def confluence_to_slack():
    data = request.json
    required_fields = ["update_type", "page_title", "page_url", "author"]

    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    result = bridge_confluence_to_slack(
        update_type=data["update_type"],
        page_title=data["page_title"],
        page_url=data["page_url"],
        author=data["author"],
        comment=data.get("comment", "")
    )

    return jsonify(result), 200 if result["success"] else 500