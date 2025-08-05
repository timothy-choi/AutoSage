from flask import Blueprint, request, jsonify
from SalesforceSchemaFieldMapperHelper import get_salesforce_field_schema

salesforce_field_schema_mapper_bp = Blueprint("salesforce_field_schema_mapper", __name__)

@salesforce_field_schema_mapper_bp.route("/salesforce/schema/map", methods=["POST"])
def map_field_schema():
    data = request.get_json()
    instance_url = data.get("instance_url")
    access_token = data.get("access_token")
    object_api_name = data.get("object_api_name")

    if not all([instance_url, access_token, object_api_name]):
        return jsonify({"success": False, "error": "Missing required parameters"}), 400

    result = get_salesforce_field_schema(instance_url, access_token, object_api_name)
    return jsonify(result), 200 if result["success"] else 500