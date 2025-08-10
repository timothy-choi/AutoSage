from flask import Blueprint, request, jsonify
from SalesforceUserCreatorHelper import create_salesforce_user

salesforce_user_creator_bp = Blueprint("salesforce_user_creator", __name__)

@salesforce_user_creator_bp.route("/salesforce/user/create", methods=["POST"])
def create_user_controller():
    data = request.json
    if not all(k in data for k in ["instance_url", "access_token", "user_data"]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = create_salesforce_user(
        instance_url=data["instance_url"],
        access_token=data["access_token"],
        user_data=data["user_data"]
    )

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code