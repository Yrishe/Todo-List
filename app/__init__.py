from flask import Flask
from .config import Config
from .models import db
from .routes import bp as main_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    # Register the main blueprint
    app.register_blueprint(main_routes)

    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    return app