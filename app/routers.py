import os
from datetime import datetime

from flask import flash, get_flashed_messages, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# 导入数据库
from app import app
from app import db
from .models import User_log

'''
登陆注册模块
'''


@app.route('/login', methods=['GET','POST'])  # 登陆
def login():
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        u_data = User_log.query.filter_by(uid=uid).first()
        if check_password_hash(u_data.password,password):
            return '登陆成功'
        else:
            return '登录失败'
    else:
        return render_template('login.html')


@app.route('/registered', methods=['GET','POST'])  # 注册
def registered():
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        # rpassword = request.form.get('rpassword')
        name = request.form.get('name')
        email = request.form.get('email')

        password = generate_password_hash(password)  # 密码加密

        user = User_log(
            uid=uid,
            password=password,
            name=name,
            email=email,
            register_login = datetime.now()
        )

        db.session.add(user)  # 向数据库添加用户信息
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('registered.html')


'''
主页
'''


@app.route('/')
@app.route('/index')  # 主页
def index():

    # 轮播区域
    post_bgs = [
        {
            'time': '2018-06-01',
            'author': 'Ming1',
            'title': 'titleA',
            'imag': '../static/images/home/01.jpg',
            'href_author': '#',
            'href_blog': '#'
        },
        {
            'time': '2018-06-02',
            'author': 'Ming2',
            'title': 'titleB',
            'imag': '../static/images/home/02.jpg',
            'href_author': '#',
            'href_blog': '#'
        }
    ]

    # 标准文章展示
    stand_as = [
        {
            'time': '2018-06-01',
            'author': 'Ming3',
            'title': '这里有非常好吃的东西',
            'like': '283',
            'view': '400',
            'comment': '20',
            'href_author': '#',
            'href_blog': '#',
            'imag': '../static/upload/images/01.jpg'
        },
        {
            'time': '2018-06-02',
            'author': 'Ming4',
            'title': '这里有非常好吃的东西+1',
            'like': '283',
            'view': '400',
            'comment': '20',
            'href_author': '#',
            'href_blog': '#',
            'imag': '../static/upload/images/02.jpg'
        }
    ]

    # 带音乐文章展示
    audio_as = [
        {
            'time': '2018-06-01',
            'author': 'Ming3',
            'title': '这里有非常好吃的东西',
            'like': '283',
            'view': '400',
            'comment': '20',
            'href_author': '#',
            'href_blog': '#',
            'imag': '../static/upload/images/03.jpeg',
            'audio': '../static/upload/audio/01.mp3'
        },
        {
            'time': '2018-06-01',
            'author': 'Ming3',
            'title': '这里有非常好吃的东西',
            'like': '283',
            'view': '400',
            'comment': '20',
            'href_author': '#',
            'href_blog': '#',
            'imag': '../static/upload/images/04.jpeg',
            'audio': '../static/upload/audio/02.mp3'
        }
    ]

    # 网站宣言
    web = {
        'quote': '网站宣言',
        'cite': '大标题'
    }

    return render_template('index.html', post_bgs=post_bgs, stand_as=stand_as, audio_as=audio_as, web=web)


'''
文章详情页及提交
'''


@app.route('/view/<blog_id>', methods=['GET', 'POST'])  # 文章详情页
def blog(blog_id):

    if request.method == 'POST':  # 当有留言提交时
        pass  # 存入数据库

    # 获取blog_id的type
    blog_type = 2

    if blog_type == 1:  # 标准文章格式

        # 获取blog
        blog = {
            'time': '2018-06-02',
            'author': 'Ming4',
            'author_imag': '../static/upload/images/02.jpg',
            'sign': '幸福生活每一天',
            'title': '这里有非常好吃的东西+1',
            'like': '283',
            'view': '400',
            'comment': '20',
            'imag': '../static/upload/images/02.jpg',
            'next_href': '#',
            'prev_href': '#',
            'next_title': '南锣鼓巷',
            'prev_title': '北京',
            'style': 'format-standard'
        }

        # comment数量
        comment_number = '5'

        # 获取comment
        comments = [
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            },
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            }
        ]

        # 返回标准页面
        return render_template('single-standard.html', blog=blog, comment_number=comment_number, comments=comments)

    # blog_type == 2
    # 音乐文章格式
    else:

        # 获取blog
        blog = {
            'time': '2018-06-02',
            'author': 'Ming4',
            'author_imag': '../static/upload/images/02.jpg',
            'sign': '幸福生活每一天',
            'title': '这里有非常好吃的东西+1',
            'like': '283',
            'view': '400',
            'comment': '20',
            'imag': '../static/upload/images/02.jpg',
            'next_href': '#',
            'prev_href': '#',
            'next_title': '南锣鼓巷',
            'prev_title': '北京',
            'audio': '../static/upload/audio/02.mp3',
            'style': 'format-audio'
        }

        # comment数量
        comment_number = '5'

        # 获取comment
        comments = [
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            },
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            }
        ]

        # 返回音乐页面
        return render_template('single-audio.html', blog=blog, comment_number=comment_number, comments=comments)


@app.route('/upload',methods=['POST','GET'])  # 文章提交页面
def user_upload():
    if request.method == 'POST':
        # title = request.form.get('title')
        # # text = request.form.get('text')
        imag = request.files['imag']
        audio = request.files['audio']
        # mp3 = request.files('mp3')
        basepath = os.path.dirname(__file__)
        upload_path_imag = os.path.join(basepath,'static/upload/images',secure_filename(imag.filename))
        upload_path_mp3 = os.path.join(basepath,'static/upload/audio',secure_filename(imag.filename))
        imag.save(upload_path_imag)
        audio.save(upload_path_mp3)
        return '上传成功'
    else:
        return render_template('upload.html')


'''
作者信息展示页面
'''


@app.route('/author/<authorname>')  # 作者详情页面
def author():
    return 1

@app.route('/example')
def example():
    return render_template('upload.html')