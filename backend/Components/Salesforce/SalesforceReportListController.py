from flask import Blueprint, request, jsonify
from SalesforceReportListHelper import list_salesforce_reports

salesforce_report_lister_bp = Blueprint("salesforce_report_lister", __name__)

@salesforce_report_lister_bp.route("/salesforce/reports/list", methods=["POST"])
def list_reports():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")

    if not all([instance_url, access_token]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = list_salesforce_reports(instance_url, access_token)
    return jsonify(result), 200 if result.get("success") else 500