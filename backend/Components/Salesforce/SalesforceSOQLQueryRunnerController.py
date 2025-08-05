from flask import Blueprint, request, jsonify
from SalesforceSOQLQueryRunnerHelper import run_soql_query

salesforce_soql_query_runner_bp = Blueprint("salesforce_soql_query_runner", __name__)

@salesforce_soql_query_runner_bp.route("/salesforce/soql/query", methods=["POST"])
def run_query():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    query = data.get("query")

    if not all([instance_url, access_token, query]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = run_soql_query(instance_url, access_token, query)
    return jsonify(result), 200 if result.get("success") else 500