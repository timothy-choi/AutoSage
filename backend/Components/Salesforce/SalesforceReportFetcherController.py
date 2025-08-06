from flask import Blueprint, request, jsonify
from SalesforceReportFetcherHelper import fetch_salesforce_report

salesforce_report_fetcher_bp = Blueprint("salesforce_report_fetcher", __name__)

@salesforce_report_fetcher_bp.route("/salesforce/reports/fetch", methods=["POST"])
def fetch_report():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    report_id = data.get("report_id")
    include_details = data.get("include_details", False)

    if not all([instance_url, access_token, report_id]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = fetch_salesforce_report(instance_url, access_token, report_id, include_details)
    return jsonify(result), 200 if result.get("success") else 500