from flask import Flask
from extensions import db, ma, api
from config import Config
from resources.syllabus import blp as SyllabusBlueprint
from flask import jsonify
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    api.register_blueprint(SyllabusBlueprint)

    # -------------------------
    # 共通エラーハンドリング
    # -------------------------
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "error": e.name,
            "message": e.description,
            "status": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {
            "error": "Internal Server Error",
            "message": str(e),
            "status": 500
        }
        return jsonify(response), 500

    return app

if __name__ == "__main__":
    app.run(debug=True)