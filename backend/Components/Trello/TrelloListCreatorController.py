from flask import Blueprint, request, jsonify
from TrelloListCreatorHelper import create_trello_list

trello_list_creator_bp = Blueprint("trello_list_creator", __name__)

@trello_list_creator_bp.route("/trello/list/create", methods=["POST"])
def trello_list_creator():
    try:
        data = request.get_json()

        result = create_trello_list(
            api_key=data["api_key"],
            token=data["token"],
            board_id=data["board_id"],
            name=data["name"],
            pos=data.get("pos", "bottom")
        )

        return jsonify({"success": True, "list": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500