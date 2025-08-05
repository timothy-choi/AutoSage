from flask import Blueprint, request, jsonify
from SalesforceSOSLQueryRunnerHelper import run_sosl_query

salesforce_sosl_query_runner_bp = Blueprint("salesforce_sosl_query_runner", __name__)

@salesforce_sosl_query_runner_bp.route("/salesforce/sosl/query", methods=["POST"])
def run_query():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    sosl = data.get("sosl")

    if not all([instance_url, access_token, sosl]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = run_sosl_query(instance_url, access_token, sosl)
    return jsonify(result), 200 if result.get("success") else 500