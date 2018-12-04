from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT


class User_info(db.Model):  # 用户信息表

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    uid = db.Column(db.String(225), unique=True)
    password = db.Column(db.String(225))
    name = db.Column(db.String(225))
    email = db.Column(db.String(225))
    sign = db.Column(LONGTEXT)
    icon = db.Column(db.String(225))
    register_login = db.Column(db.DateTime())  # 注册时间

    def __init__(self, uid, password, name, icon, sign, email, register_login):
        self.uid = uid
        self.password = password
        self.name = name
        self.email = email
        self.sign = sign
        self.icon = icon
        self.register_login = register_login

    def __repr__(self):
        return "<user uid '{}'>".format(self.uid)


class Blog_info(db.Model):  # 博客信息表

    __tablename__ = 'blog_info'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(225))
    blog_markdown = db.Column(db.Text)
    imag = db.Column(db.String(225))
    audio = db.Column(db.String(225))
    blog_type = db.Column(db.Integer)
    upload_time = db.Column(db.DateTime())
    blog_timeid = db.Column(db.String(225))
    user_id = db.Column(db.String(225), db.ForeignKey('user_info.uid'))

    def __init__(self, title, blog_markdown, imag, audio, blog_type, upload_time, blog_timeid, user_id):
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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    comment = db.Column(db.String(225))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_info.id'))
    user_id = db.Column(db.String(225), db.ForeignKey('user_info.uid'))
    upload_time = db.Column(db.DateTime())

    def __init__(self, comment, blog_id, user_id, upload_time):
        self.comment = comment
        self.blog_id = blog_id
        self.user_id = user_id
        self.upload_time = upload_time

    def __repr__(self):
        return "<comment id '{}'>".format(self.id)


class Pictures(db.Model):  # 插画集

    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(225))
    text = db.Column(db.String(225))
    ad = db.Column(db.String(225))
    imag = db.Column(db.String(225))

    def __init__(self, name, text, ad, imag):
        self.name = name
        self.text = text
        self.ad = ad
        self.imag = imag

    def __repr__(self):
        return "<pictures id '{}'>".format(self.id)

class Books(db.Model):

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(225))
    style = db.Column(db.String(225))
    num = db.Column(db.String(225))
    text = db.Column(db.Text)
    time = db.Column(db.String(225))
    bottom = db.Column(db.String(225))
    read = db.Column(LONGTEXT)
    imag = db.Column(db.String(225))
    imagf = db.Column(db.String(225))

    def __init__(self,title,style,num,text,time,bottom,read,imag,imagf):
        self.title = title
        self.style = style
        self.num = num
        self.text = text
        self.time = time
        self.bottom = bottom
        self.read = read
        self.imag = imag
        self.imagf = imagf
    
    def __repr__(self):
        return "<books id '{}'>".format(self.id)

class Music(db.Model):

    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(225))
    time = db.Column(db.String(225))
    singer = db.Column(db.String(225))
    album = db.Column(db.String(225))
    side1 = db.Column(db.Text)
    side2 = db.Column(db.Text)

    def __init__(self,name,time,singer,album,side1,side2):
        self.name = name
        self.time = time
        self.singer = singer
        self.album = album
        self.side1 = side1
        self.side2 = side2

    def __repr__(self):
        return "<music id '{}'>".format(self.id)