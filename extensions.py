from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_smorest import Api

db = SQLAlchemy()
ma = Marshmallow()
api = Api()