from flask import Blueprint, request, jsonify
from ConfluenceToGithubSyncerHelper import sync_confluence_to_github

confluence_to_github_syncer_bp = Blueprint("confluence_to_github_syncer", __name__)

@confluence_to_github_syncer_bp.route("/confluence/to_github", methods=["POST"])
def confluence_to_github():
    data = request.get_json()
    required_fields = ["page_id", "owner", "repo", "filepath"]
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    result = sync_confluence_to_github(
        page_id=data["page_id"],
        owner=data["owner"],
        repo=data["repo"],
        filepath=data["filepath"],
        branch=data.get("branch", "main")
    )

    return jsonify(result), 200 if result.get("success") else 500