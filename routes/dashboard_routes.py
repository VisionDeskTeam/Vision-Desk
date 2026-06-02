from flask import Blueprint, render_template, jsonify
from services.log_service import get_user_logs

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def dashboard():
    """Renders the main dashboard HTML page."""
    return render_template("dashboard.html")


@dashboard_bp.route("/api/veriler", methods=["GET"])
def veriler():
    """
    Returns aggregated focus & posture data for the dashboard.

    Response format:
        [{"focus": <int>, "posture": <int>}]

    get_user_logs() returns a dict: {"focus": <int>, "posture": <int>}
    Adjust user_id as needed for your use-case.
    """
    try:
        # Returns dict: {"posture": <total>, "focus": <total>}
        data = get_user_logs(user_id=1)

        if not data:
            return jsonify([{"focus": 0, "posture": 0}])

        payload = {
            "focus":   int(data.get("focus",   0)),
            "posture": int(data.get("posture", 0)),
        }
        return jsonify([payload])

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
