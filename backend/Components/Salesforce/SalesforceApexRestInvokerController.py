from flask import Blueprint, request, jsonify
from SalesforceApexRestInvokerHelper import invoke_apex_rest

salesforce_apex_rest_invoker_bp = Blueprint("salesforce_apex_rest_invoker", __name__)

@salesforce_apex_rest_invoker_bp.route("/salesforce/apex-rest/invoke", methods=["POST"])
def invoke_apex():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    endpoint_path = data.get("endpoint_path")
    method = data.get("method", "GET")
    payload = data.get("payload", None)
    params = data.get("params", None)

    if not all([instance_url, access_token, endpoint_path]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = invoke_apex_rest(instance_url, access_token, endpoint_path, method, payload, params)
    return jsonify(result), 200 if result.get("success") else 500