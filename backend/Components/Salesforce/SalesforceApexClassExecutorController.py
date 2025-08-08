from flask import Blueprint, request, jsonify
from SalesforceApexClassExecutorHelper import execute_apex_anonymous

salesforce_apex_class_executor_bp = Blueprint("salesforce_apex_class_executor", __name__)

@salesforce_apex_class_executor_bp.route("/salesforce/apex-class/execute", methods=["POST"])
def execute_apex_class():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    apex_code = data.get("apex_code")

    if not all([instance_url, access_token, apex_code]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = execute_apex_anonymous(instance_url, access_token, apex_code)
    return jsonify(result), 200 if result.get("success") else 500