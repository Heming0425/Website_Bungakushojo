from app import db
from datetime import datetime


class User_info(db.Model): #用户信息表

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(225), unique=True)
    password = db.Column(db.String(225))
    name = db.Column(db.String(225))
    email = db.Column(db.String(225))
    register_login = db.Column(db.DateTime())  # 注册时间

    def __init__(self, uid, password, name, email, register_login):
        self.uid = uid
        self.password = password
        self.name = name
        self.email = email
        self.register_login = register_login

    def __repr__(self):
        return "<model uid '{}'>".format(self.uid)


class Blog_info(db.Model): #博客信息表

    __tablename__ = 'blog_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225))
    text = db.Column(db.String(225))
    imag = db.Column(db.String(225))
    audio = db.Column(db.String(225))
    blog_type = db.Column(db.Integer)
    upload_time = db.Column(db.DateTime())
    user_id = db.Column(db.String(225), db.ForeignKey('user_info.uid'))

    def __init__(self, title, text, imag, audio, blog_type,upload_time, user_id):
        self.title = title
        self.text = text
        self.imag = imag
        self.audio = audio
        self.blog_type = blog_type
        self.user_id = user_id
        self.upload_time = upload_time
