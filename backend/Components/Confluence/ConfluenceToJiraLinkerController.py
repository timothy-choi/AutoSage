from flask import Blueprint, request, jsonify
from ConfluenceToJiraLinkerHelper import link_confluence_to_jira

confluence_to_jira_linker_bp = Blueprint("confluence_to_jira_linker", __name__)

@confluence_to_jira_linker_bp.route("/confluence/link_to_jira", methods=["POST"])
def link_to_jira():
    data = request.get_json()
    required_fields = {"page_id", "jira_issue_key", "confluence_base_url"}
    if not required_fields.issubset(data):
        return jsonify({"success": False, "error": "Missing one or more required fields"}), 400

    result = link_confluence_to_jira(
        page_id=data["page_id"],
        jira_issue_key=data["jira_issue_key"],
        confluence_base_url=data["confluence_base_url"]
    )
    return jsonify(result), 200 if result.get("success") else 500