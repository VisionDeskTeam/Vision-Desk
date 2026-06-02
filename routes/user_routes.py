from flask import Blueprint, request, jsonify
from services.user_service import login_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    result = login_user(data["username"], data["password"])
    return jsonify(result)