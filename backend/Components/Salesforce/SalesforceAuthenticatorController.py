from flask import Blueprint, request, jsonify
from SalesforceAuthenticatorHelper import (
    authenticate_with_username_password,
    authenticate_with_refresh_token
)

salesforce_authenticator_bp = Blueprint("salesforce_authenticator", __name__)

@salesforce_authenticator_bp.route("/salesforce/authenticate", methods=["POST"])
def authenticate_salesforce():
    data = request.get_json()
    auth_type = data.get("auth_type")

    if auth_type == "password":
        required_keys = ["client_id", "client_secret", "username", "password", "security_token"]
        if not all(k in data for k in required_keys):
            return jsonify({"success": False, "error": "Missing required fields for password flow"}), 400

        result = authenticate_with_username_password(
            data["client_id"],
            data["client_secret"],
            data["username"],
            data["password"],
            data["security_token"]
        )

    elif auth_type == "refresh_token":
        required_keys = ["client_id", "client_secret", "refresh_token"]
        if not all(k in data for k in required_keys):
            return jsonify({"success": False, "error": "Missing required fields for refresh token flow"}), 400

        result = authenticate_with_refresh_token(
            data["client_id"],
            data["client_secret"],
            data["refresh_token"]
        )

    else:
        return jsonify({"success": False, "error": "Invalid auth_type"}), 400

    return jsonify(result), 200 if result["success"] else 401