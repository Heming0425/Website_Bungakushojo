import os

# 24位字符设置
SECRET_KEY = os.urandom(24)

# sql配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19980425@localhost:3306/flask_project'
SQLALCHEMY_TRACK_MODIFICATIONS = False