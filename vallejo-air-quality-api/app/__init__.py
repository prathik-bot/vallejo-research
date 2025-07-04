from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import using the correct name
    from app.routes.sensors import sensors_bp
    app.register_blueprint(sensors_bp, url_prefix='/api')

    return app