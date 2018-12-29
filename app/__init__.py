import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel

app = Flask(__name__)
babel = Babel(app) # 国际化

app.config.from_object('config')
db = SQLAlchemy(app)

from app import routers