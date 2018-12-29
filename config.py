import os

# 24位字符设置
SECRET_KEY = os.urandom(24)

# sql配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19980425@localhost:3306/basic_blog'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 国际化
BABEL_DEFAULT_LOCALE = 'zh_CN'
