from flask import Blueprint, request, jsonify
from TrelloCardMoverHelper import move_trello_card

trello_card_mover_bp = Blueprint("trello_card_mover", __name__)

@trello_card_mover_bp.route("/trello/card/move", methods=["POST"])
def trello_card_mover():
    try:
        data = request.get_json()

        result = move_trello_card(
            api_key=data["api_key"],
            token=data["token"],
            card_id=data["card_id"],
            target_list_id=data["target_list_id"]
        )

        return jsonify({"success": True, "moved_card": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500