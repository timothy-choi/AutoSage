from flask import Blueprint, request, jsonify
from SalesforceConnectionTesterHelper import test_salesforce_connection

salesforce_connection_tester_bp = Blueprint("salesforce_connection_tester", __name__)

@salesforce_connection_tester_bp.route("/salesforce/test-connection", methods=["POST"])
def test_connection():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")

    if not instance_url or not access_token:
        return jsonify({
            "success": False,
            "error": "Both instance_url and access_token are required"
        }), 400

    result = test_salesforce_connection(instance_url, access_token)
    return jsonify(result), 200 if result["success"] else 401