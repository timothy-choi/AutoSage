from flask import Blueprint, request, jsonify
from TrelloLabelCreatorHelper import create_label

trello_label_creator_bp = Blueprint("trello_label_creator", __name__)

@trello_label_creator_bp.route("/trello/label/create", methods=["POST"])
def trello_label_creator():
    try:
        data = request.get_json()

        label = create_label(
            api_key=data["api_key"],
            token=data["token"],
            board_id=data["board_id"],
            label_name=data["label_name"],
            label_color=data["label_color"]
        )

        return jsonify({"success": True, "label": label})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500