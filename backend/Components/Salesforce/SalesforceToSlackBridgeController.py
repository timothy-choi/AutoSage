from flask import Blueprint, request, jsonify
from SalesforceToSlackBridgeHelper import send_salesforce_event_to_slack

salesforce_to_slack_bridge_bp = Blueprint("salesforce_to_slack_bridge", __name__)

@salesforce_to_slack_bridge_bp.route("/salesforce/to/slack", methods=["POST"])
def salesforce_to_slack():
    data = request.json
    slack_webhook_url = data.get("slack_webhook_url")

    if not slack_webhook_url:
        return jsonify({"success": False, "error": "Missing Slack webhook URL"}), 400

    result = send_salesforce_event_to_slack(slack_webhook_url, data)
    return jsonify(result), (200 if result["success"] else 500)