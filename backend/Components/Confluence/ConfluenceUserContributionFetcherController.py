from flask import Blueprint, request, jsonify
from ConfluenceUserContributionFetcherHelper import get_user_contributions

confluence_user_contribution_fetcher_bp = Blueprint("confluence_user_contribution_fetcher", __name__)

@confluence_user_contribution_fetcher_bp.route("/confluence/user_contributions", methods=["POST"])
def user_contributions():
    data = request.get_json()
    user_account_id = data.get("user_account_id")
    limit = data.get("limit", 25)

    if not user_account_id:
        return jsonify({"success": False, "error": "Missing user_account_id"}), 400

    result = get_user_contributions(user_account_id, limit)
    return jsonify(result), 200 if result.get("success") else 500
