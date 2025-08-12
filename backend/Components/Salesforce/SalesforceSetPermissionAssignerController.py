from flask import Blueprint, request, jsonify
from SalesforceSetPermissionAssignerHelper import assign_permission_set

salesforce_permission_set_assigner_bp = Blueprint("salesforce_permission_set_assigner", __name__)

@salesforce_permission_set_assigner_bp.route("/salesforce/permission-set/assign", methods=["POST"])
def assign_permission_set_controller():
    data = request.json
    required_fields = ["instance_url", "access_token", "user_id", "permission_set_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = assign_permission_set(
        instance_url=data["instance_url"],
        access_token=data["access_token"],
        user_id=data["user_id"],
        permission_set_id=data["permission_set_id"]
    )

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code