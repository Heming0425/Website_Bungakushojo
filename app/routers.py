import os
from datetime import datetime

from flask import flash, get_flashed_messages, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# 导入数据库
from app import app
from app import db
from .models import User_info, Blog_info, Comment_info

'''
登陆注册模块
'''


@app.route('/login', methods=['GET', 'POST'])  # 登陆
def login():
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        u_data = User_info.query.filter_by(uid=uid).first()
        try:
            rp = u_data.password
            if check_password_hash(rp, password):
                session['uid'] = uid
                return redirect('index')
            else:
                flash('密码错误')
                return render_template('login.html', flash=flash)
        except:
            flash('用户不存在')
            return render_template('login.html', flash=flash)
    else:
        return render_template('login.html')


@app.route('/registered', methods=['GET', 'POST'])  # 注册
def registered():
    if request.method == 'POST':

        uid = request.form.get('uid')  # 验证用户名
        try:
            if User_info.query.filter_by(uid=uid).first().uid:
                flash('该用户名存在')
                return render_template('registered.html', flash=flash)
        except:
            pass

        password = request.form.get('password')
        rpassword = request.form.get('rpassword')

        if password != rpassword:  # 验证密码
            flash('两次密码不一致')
            render_template('registered.html', flash=flash)
        name = request.form.get('name')
        email = request.form.get('email')

        password = generate_password_hash(password)  # 密码加密

        user = User_info(
            uid=uid,
            password=password,
            name=name,
            email=email,
            sign='这个人什么也没留下Orz',  # 注册时默认
            icon='upload/icon/default.jpg',
            register_login=datetime.now()
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

    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)

    # 轮播设置

    post_bg1 = Blog_info.query.filter_by(id='1').first()
    post_bg2 = Blog_info.query.filter_by(id='2').first()
    post_bg3 = Blog_info.query.filter_by(id='3').first()
    post_bg4 = Blog_info.query.filter_by(id='4').first()
    post_bgs = [post_bg1, post_bg2, post_bg3, post_bg4]

    post_bg1_author = User_info.query.filter_by(uid=post_bg1.user_id).first()
    post_bg2_author = User_info.query.filter_by(uid=post_bg2.user_id).first()
    post_bg3_author = User_info.query.filter_by(uid=post_bg3.user_id).first()
    post_bg4_author = User_info.query.filter_by(uid=post_bg4.user_id).first()
    post_bgs_author = [post_bg1_author, post_bg2_author,
                       post_bg3_author, post_bg4_author]

    posts = zip(post_bgs, post_bgs_author)

    # 标准文章展示

    # 例子
    post_stand1 = Blog_info.query.filter_by(id='1').first()
    post_stand2 = Blog_info.query.filter_by(id='2').first()
    post_stand = [post_stand1, post_stand2]

    post_stand_author1 = User_info.query.filter_by(
        uid=post_stand1.user_id).first()
    post_stand_author2 = User_info.query.filter_by(
        uid=post_stand2.user_id).first()
    post_stand_author = [post_stand_author1, post_stand_author2]

    stand_zip = zip(post_stand, post_stand_author)

    # 带音乐文章展示
    post_audio1 = Blog_info.query.filter_by(id='3').first()
    post_audio = [post_audio1]

    post_audio_author1 = User_info.query.filter_by(
        uid=post_audio1.user_id).first()
    post_audio_author = [post_audio_author1]

    audio_zip = zip(post_audio, post_audio_author)

    return render_template('index.html', posts=posts, stand_zip=stand_zip, audio_zip=audio_zip)


'''
文章详情页及提交
'''


@app.route('/view/<blog_id>', methods=['GET', 'POST'])  # 文章详情页
def view(blog_id):
    
    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)
    
    if request.method == 'POST':  # 当有留言提交时
        comment = request.form.get('comment')
        c = Comment_info(
            comment = comment,
            blog_id = blog_id,
            user_id = session['uid'],
            upload_time = datetime.now()
        )
        db.session.add(c)  # 向数据库添加用户信息
        db.session.commit()
    
    
    # 获取comment
    comments = Comment_info.query.filter_by(blog_id=blog_id).all()

    authors = []
    if comments is not None:
        for comment in comments:
            authors.append(User_info.query.filter_by(uid=comment.user_id).first())
    
    comment_zip = zip(comments, authors)

    # comment数量
    comment_number = len(comments)
    
    blog_data = Blog_info.query.filter_by(id=blog_id).first()  # 获取文章信息
    author_data = User_info.query.filter_by(
        uid=blog_data.user_id).first()  # 获取文章对应的author信息

    if blog_data.blog_type == 1:  # 标准文章格式
        view = {
            'style': 'format-standard'
        }
        return render_template('single-standard.html', blog=blog_data, comment_number=comment_number, comment_zip=comment_zip, author=author_data, view=view)
    else:  # 音乐文章格式
        view = {
            'style': 'format-audio'
        }
        return render_template('single-audio.html', blog=blog_data, comment_number=comment_number, comment_zip=comment_zip, author=author_data, view=view)


@app.route('/upload', methods=['POST', 'GET'])  # 文章提交页面
def user_upload():

    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)

    if request.method == 'POST':

        # 必要信息获取
        title = request.form.get('title')
        text = request.form.get('text')
        imag = request.files['imag']
        upload_time = datetime.now()
        blog_type = 1

        # 上传基本路径
        basepath = os.path.dirname(__file__)

        # 上传图片
        upload_path_imag = os.path.join(
            basepath, 'static/upload/images', secure_filename(imag.filename))  # 文件存入服务器
        imag.save(upload_path_imag)
        upload_path_imag = os.path.join(
            'upload/images', secure_filename(imag.filename))  # 路径存入数据库

        # 是否上传音乐
        try:
            audio = request.files['audio']
            upload_path_mp3 = os.path.join(
                basepath, 'static/upload/audio', secure_filename(audio.filename))
            audio.save(upload_path_mp3)
            upload_path_mp3 = os.path.join(
                'upload/audio', secure_filename(audio.filename))
            blog_type = 2
        except:
            upload_path_mp3 = None

        blog = Blog_info(
            title=title,
            text=text,
            imag=upload_path_imag,
            audio=upload_path_mp3,
            blog_type=blog_type,
            upload_time=upload_time,
            user_id=uid  # 外键指向uid
        )

        db.session.add(blog)
        db.session.commit()

        return redirect('index')

    else:
        return render_template('upload.html')


'''
作者信息展示页面
'''


@app.route('/author/<authoruid>', methods=['GET', 'POST'])  # 作者信息展示页面
def author(authoruid):

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        sign = request.form.get('sign')
        icon = request.files['icon']

        # 上传基本路径
        basepath = os.path.dirname(__file__)

        # 上传作者头像
        upload_path_icon = os.path.join(
            basepath, 'static/upload/icon', secure_filename(icon.filename))  # 文件存入服务器
        icon.save(upload_path_icon)
        upload_path_icon = os.path.join(
            'upload/icon', secure_filename(icon.filename))
        User_info.query.filter_by(uid=session['uid']).update({  # 更新
            'name': name,
            'email': email,
            'sign': sign,
            'icon': upload_path_icon
        })
        db.session.commit()

    # 验证登陆
    # 验证当前用户是否匹配以显示change
    change = None
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html')
    if uid == authoruid:
        change = 1

    u_data = User_info.query.filter_by(uid=authoruid).first()
    blogs = Blog_info.query.filter_by(user_id=authoruid).all()

    # 验证u_data
    # 前端检验blogs
    return render_template('author_info.html', author=u_data, blogs=blogs, change=change)
