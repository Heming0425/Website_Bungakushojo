from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT


class User_info(db.Model): #用户信息表

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True,unique=True)
    uid = db.Column(db.String(225), unique=True)
    password = db.Column(db.String(225))
    name = db.Column(db.String(225))
    email = db.Column(db.String(225))
    sign = db.Column(LONGTEXT)
    icon = db.Column(db.String(225))
    register_login = db.Column(db.DateTime())  # 注册时间

    def __init__(self, uid, password, name,icon,sign, email, register_login):
        self.uid = uid
        self.password = password
        self.name = name
        self.email = email
        self.sign = sign
        self.icon = icon
        self.register_login = register_login

    def __repr__(self):
        return "<user uid '{}'>".format(self.uid)


class Blog_info(db.Model): #博客信息表

    __tablename__ = 'blog_info'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    title = db.Column(db.String(225))
    blog_markdown = db.Column(db.Text)
    imag = db.Column(db.String(225))
    audio = db.Column(db.String(225))
    blog_type = db.Column(db.Integer)
    upload_time = db.Column(db.DateTime())
    blog_timeid = db.Column(db.String(225))
    user_id = db.Column(db.String(225), db.ForeignKey('user_info.uid'))

    def __init__(self, title, blog_markdown, imag, audio, blog_type,upload_time,blog_timeid, user_id):
        self.title = title
        self.blog_markdown = blog_markdown
        self.imag = imag
        self.audio = audio
        self.blog_type = blog_type
        self.user_id = user_id
        self.upload_time = upload_time
        self.blog_timeid = blog_timeid

    def __repr__(self):
        return "<blog id '{}'>".format(self.id)

class Comment_info(db.Model):

    __tablename__ = 'comment_info'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    comment = db.Column(db.String(225))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_info.id'))
    user_id = db.Column(db.String(225), db.ForeignKey('user_info.uid'))
    upload_time = db.Column(db.DateTime())

    def __init__(self, comment, blog_id, user_id,upload_time):
        self.comment = comment
        self.blog_id = blog_id
        self.user_id = user_id
        self.upload_time = upload_time
    
    def __repr__(self):
        return "<comment id '{}'>".format(self.id)

