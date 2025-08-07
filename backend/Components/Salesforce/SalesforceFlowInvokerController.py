from flask import Blueprint, request, jsonify
from SalesforceFlowInvokerHelper import invoke_salesforce_flow

salesforce_flow_invoker_bp = Blueprint("salesforce_flow_invoker", __name__)

@salesforce_flow_invoker_bp.route("/salesforce/flows/invoke", methods=["POST"])
def invoke_flow():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    flow_name = data.get("flow_name")
    input_variables = data.get("input_variables", {})

    if not all([instance_url, access_token, flow_name]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = invoke_salesforce_flow(instance_url, access_token, flow_name, input_variables)
    return jsonify(result), 200 if result.get("success") else 500