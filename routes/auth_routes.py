from flask import Blueprint, render_template, jsonify, request
from services.user_service import login_user

auth_bp = Blueprint("auth", __name__)


# ── GET pages ────────────────────────────────
@auth_bp.route("/login", methods=["GET"])
def login():
    """Renders the login page (user + admin toggle)."""
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET"])
def register():
    """Renders the registration page."""
    return render_template("register.html")


# ── POST endpoints ────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login_post():
    """
    Authenticates a user or admin.

    Request JSON:  {"username": "...", "password": "..."}
    Response JSON: {"status": "success", "user_id": <int>, "role": "admin"|"user"}
                or {"status": "fail"}
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"status": "fail", "message": "Kullanıcı adı ve şifre gerekli."}), 400

    result = login_user(username, password)
    return jsonify(result)


@auth_bp.route("/register", methods=["POST"])
def register_post():
    """
    Creates a new user account.

    Request JSON:  {"firstname": "...", "lastname": "...",
                    "username": "...", "email": "...", "password": "..."}
    Response JSON: {"status": "success"} | {"status": "fail", "message": "..."}

    NOTE: Implement the actual DB insert in services/user_service.py
          (register_user function) and import it here.
    """
    data = request.get_json(silent=True) or {}

    required = ["firstname", "lastname", "username", "email", "password"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({
                "status": "fail",
                "message": f"'{field}' alanı zorunludur."
            }), 400

    # TODO: call register_user(data) from user_service once implemented
    # from services.user_service import register_user
    # result = register_user(data)
    # return jsonify(result)

    # Placeholder response — replace with real DB call:
    return jsonify({
        "status": "success",
        "message": "Hesap oluşturuldu."
    })
