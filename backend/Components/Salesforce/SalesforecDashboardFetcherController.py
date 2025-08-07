from flask import Blueprint, request, jsonify
from SalesforceDashboardFetcherHelper import fetch_salesforce_dashboard

salesforce_dashboard_fetcher_bp = Blueprint("salesforce_dashboard_fetcher", __name__)

@salesforce_dashboard_fetcher_bp.route("/salesforce/dashboards/fetch", methods=["POST"])
def fetch_dashboard():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    dashboard_id = data.get("dashboard_id")

    if not all([instance_url, access_token, dashboard_id]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = fetch_salesforce_dashboard(instance_url, access_token, dashboard_id)
    return jsonify(result), 200 if result.get("success") else 500