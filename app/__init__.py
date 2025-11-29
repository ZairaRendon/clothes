from flask import Flask
from .routes.main import main_bp

def crate_app():
    app = Flask(__name__)
    

    //registro de blueprints

    app.register_blueprint(main_bp)


    return app


