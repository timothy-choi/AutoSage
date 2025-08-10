from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from SalesforceSalesDownloaderHelper import download_file_from_salesforce

salesforce_file_downloader_bp = Blueprint("salesforce_file_downloader", __name__)

@salesforce_file_downloader_bp.route("/salesforce/file/download", methods=["GET"])
def download_file_controller():
    instance_url = request.args.get("instance_url")
    access_token = request.args.get("access_token")
    content_document_id = request.args.get("content_document_id")

    if not all([instance_url, access_token, content_document_id]):
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    result = download_file_from_salesforce(instance_url, access_token, content_document_id)

    if not result.get("success"):
        return jsonify(result), 500

    return send_file(
        BytesIO(result["file_data"]),
        as_attachment=True,
        download_name=result["file_name"],
        mimetype=result["content_type"]
    )