from flask import Blueprint, request, jsonify
from ConfluenceContentTreeExporterHelper import export_content_tree

confluence_content_tree_exporter_bp = Blueprint("confluence_content_tree_exporter", __name__)

@confluence_content_tree_exporter_bp.route("/confluence/export_content_tree", methods=["GET"])
def export_tree():
    space_key = request.args.get("space_key")
    root_page_id = request.args.get("root_page_id")

    result = export_content_tree(space_key=space_key, root_page_id=root_page_id)
    return jsonify(result), 200 if result["success"] else 400
