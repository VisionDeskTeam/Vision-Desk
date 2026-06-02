from models.log_model import get_logs_by_user

def get_user_logs(user_id):
    logs = get_logs_by_user(user_id)

    total_posture = 0
    total_focus = 0

    for log in logs:
        total_posture += log[0]
        total_focus += log[1]

    return {
        "posture": total_posture,
        "focus": total_focus  # dakika
    }