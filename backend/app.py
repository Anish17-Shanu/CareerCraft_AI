from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    from routes.catalog_routes import catalog_bp
    from routes.external_routes import external_bp
    from routes.recommendation_routes import recommendation_bp
    from routes.question_routes import question_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(external_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(question_bp)

    @app.get("/health")
    def health():
        db_status = "ok"
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            db_status = "unavailable"

        return jsonify(
            {
                "service": "CareerCraft AI backend",
                "status": "ok",
                "database": db_status,
            }
        )

    @app.get("/")
    def root():
        return jsonify(
            {
                "service": "CareerCraft AI backend",
                "status": "running",
                "health": "/health",
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
    )
