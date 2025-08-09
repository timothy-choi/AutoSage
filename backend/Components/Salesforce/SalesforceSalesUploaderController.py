from flask import Blueprint, request, jsonify
from SalesforceSalesUploaderHelper import upload_file_to_salesforce

salesforce_file_uploader_bp = Blueprint("salesforce_file_uploader", __name__)

@salesforce_file_uploader_bp.route("/salesforce/file/upload", methods=["POST"])
def upload_file_controller():
    instance_url = request.form.get("instance_url")
    access_token = request.form.get("access_token")
    linked_record_id = request.form.get("linked_record_id")
    file = request.files.get("file")

    if not all([instance_url, access_token, linked_record_id, file]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = upload_file_to_salesforce(
        instance_url=instance_url,
        access_token=access_token,
        file_name=file.filename,
        file_data=file.read(),
        linked_record_id=linked_record_id
    )

    return jsonify(result), 200 if result.get("success") else 500