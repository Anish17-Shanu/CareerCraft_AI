from flask import Flask
from config import Config
from database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes.catalog_routes import catalog_bp
    from routes.external_routes import external_bp
    from routes.recommendation_routes import recommendation_bp
    from routes.question_routes import question_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(external_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(question_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
