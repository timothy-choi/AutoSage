from flask import Blueprint, request, jsonify
from TrelloCardArchiverHelper import archive_trello_card

trello_card_archiver_bp = Blueprint("trello_card_archiver", __name__)

@trello_card_archiver_bp.route("/trello/card/archive", methods=["POST"])
def trello_card_archiver():
    try:
        data = request.get_json()

        result = archive_trello_card(
            api_key=data["api_key"],
            token=data["token"],
            card_id=data["card_id"]
        )

        return jsonify({"success": True, "card": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500