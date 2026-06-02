from flask import Flask
from routes.user_routes import user_bp
from routes.log_routes import log_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



#app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(log_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)