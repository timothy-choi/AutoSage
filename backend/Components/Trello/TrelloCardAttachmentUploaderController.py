from flask import Blueprint, request, jsonify
from TrelloCardAttachmentUploaderHelper import upload_file_attachment, attach_url
import os

trello_card_attachment_uploader_bp = Blueprint("trello_card_attachment_uploader", __name__)

@trello_card_attachment_uploader_bp.route("/trello/card/attachment/upload", methods=["POST"])
def upload_attachment():
    try:
        if request.content_type.startswith("multipart/form-data"):
            # File upload case
            api_key = request.form["api_key"]
            token = request.form["token"]
            card_id = request.form["card_id"]
            uploaded_file = request.files["file"]

            temp_path = f"/tmp/{uploaded_file.filename}"
            uploaded_file.save(temp_path)

            result = upload_file_attachment(api_key, token, card_id, temp_path)

            os.remove(temp_path)
            return jsonify({"success": True, "attachment": result})

        else:
            # URL attachment case
            data = request.get_json()
            api_key = data["api_key"]
            token = data["token"]
            card_id = data["card_id"]
            url_to_attach = data["url"]
            name = data.get("name")

            result = attach_url(api_key, token, card_id, url_to_attach, name)
            return jsonify({"success": True, "attachment": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500