from flask import Blueprint, request, jsonify
from ConfluenceSpaceDeleterHelper import delete_confluence_space

confluence_space_deleter_bp = Blueprint("confluence_space_deleter", __name__)

@confluence_space_deleter_bp.route("/confluence/delete_space", methods=["DELETE"])
def delete_space():
    data = request.get_json()
    space_key = data.get("space_key")

    if not space_key:
        return jsonify({"success": False, "message": "Missing 'space_key' in request body"}), 400

    result = delete_confluence_space(space_key)
    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code