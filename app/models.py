from app import db
from datetime import datetime

class User(db.Model):

    # 表名
    __tablename__ = 't_user'

    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(225),unique=True)
    password = db.Column(db.String(225))
    name = db.Column(db.String(225))
    register_login = db.Column(db.DateTime())

    def __init__(self, uid, password, name,register_login):
        self.uid = uid
        self.password = password
        self.name = name
        self.register_login = register_login
    
    def __repr__(self):
        return "<model uid '{}'>".format(self.uid)