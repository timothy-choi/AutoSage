from flask import Blueprint, request, jsonify
from TrelloCardWatcherHelper import set_card_watch

trello_card_watcher_bp = Blueprint("trello_card_watcher", __name__)

@trello_card_watcher_bp.route("/trello/card/watch", methods=["POST"])
def watch_card():
    try:
        data = request.get_json()
        api_key = data["api_key"]
        token = data["token"]
        card_id = data["card_id"]
        watch = data.get("watch", True)

        result = set_card_watch(api_key, token, card_id, watch)
        return jsonify({"success": True, "watched": result.get("value", watch)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500