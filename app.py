from flask import Flask
from extensions import db, ma, api
from config import Config
from resources.syllabus import blp as SyllabusBlueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    api.register_blueprint(SyllabusBlueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)