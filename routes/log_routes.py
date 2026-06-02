from flask import Blueprint, jsonify
from services.log_service import get_user_logs

log_bp = Blueprint("log", __name__)

@log_bp.route("/logs/<int:user_id>", methods=["GET"])
def logs(user_id):
    data = get_user_logs(user_id)
    return jsonify(data)