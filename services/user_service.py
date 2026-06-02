from models.user_model import get_user

def login_user(username, password):
    user = get_user(username, password)

    if user:
        return {
            "status": "success",
            "user_id": user[0],
            "role": user[3]
        }
    else:
        return {"status": "fail"}