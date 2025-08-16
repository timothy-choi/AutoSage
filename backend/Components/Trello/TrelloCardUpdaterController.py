from flask import Blueprint, request, jsonify
from TrelloCardUpdaterHelper import update_trello_card

trello_card_updater_bp = Blueprint("trello_card_updater", __name__)

@trello_card_updater_bp.route("/trello/card/update", methods=["POST"])
def trello_card_updater():
    try:
        data = request.get_json()

        updated_card = update_trello_card(
            api_key=data["api_key"],
            token=data["token"],
            card_id=data["card_id"],
            updates=data["updates"]
        )

        return jsonify({"success": True, "updated_card": updated_card})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500