import os
import random
from datetime import datetime

from flask import flash, get_flashed_messages, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, Response

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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])  # 主页
def index():

    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)

    # 轮播设置
    post_id = [1]  # 轮播文章选择
    post_bgs = []
    post_bgs_author = []
    for i in post_id:
        post_bg = Blog_info.query.filter_by(id=i).first()
        post_bg_author = User_info.query.filter_by(uid=post_bg.user_id).first()
        post_bgs.append(post_bg)
        post_bgs_author.append(post_bg_author)
    posts = zip(post_bgs, post_bgs_author)

    # 文章展示
    blog_ids = [1, 2, 3]
    post_blogs = []
    post_blogs_author = []
    for i in blog_ids:
        post_blog = Blog_info.query.filter_by(id=i).first()
        author = User_info.query.filter_by(uid=post_blog.user_id).first()
        post_blogs.append(post_blog)
        post_blogs_author.append(author)
    blog_zip = zip(post_blogs, post_blogs_author)

    return render_template('index.html', posts=posts, blog_zip=blog_zip,flash=flash)


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
            comment=comment,
            blog_id=blog_id,
            user_id=session['uid'],
            upload_time=datetime.now()
        )
        db.session.add(c)  # 向数据库添加用户信息
        db.session.commit()

    # 获取comment
    comments = Comment_info.query.filter_by(blog_id=blog_id).all()

    authors = []
    if comments is not None:
        for comment in comments:
            authors.append(User_info.query.filter_by(
                uid=comment.user_id).first())

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
    else:
        pass

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


'''
检索功能
'''


@app.route('/index/search')
def search():  # 标题关键词检索
    
    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)
    
    search_info = request.args.get('search_info')
    search_data = Blog_info.query.filter(
        Blog_info.title.like('%' + search_info + '%')).all()
    
    try:
        search_authors = []
        for i in search_data:
            author = User_info.query.filter_by(uid=i.user_id).first()
            search_authors.append(author)
            search_zip = zip(search_data, search_authors)
    except:
        pass
    
    if search_authors != []:
        search_zip = zip(search_data, search_authors)
    else:
        flash('很抱歉，没有检索到对应的信息')
        return redirect('index')
    return render_template('search.html', search_zip=search_zip)


'''
用户markdown文章上传
'''


@app.route('/markdown', methods=['GET', 'POST'])
def blog_markdown():

    # 验证session
    try:
        uid = session['uid']
    except:
        flash('请先登陆')
        return render_template('login.html', flash=flash)

    # markdown编辑
    if request.method == 'POST':

        # 获取基本信息
        title = request.form.get('title')
        blog_markdown = request.form.get('basic-editormd-html-code')
        upload_time = datetime.now()
        blog_type = 1
        blog_timeid=datetime.now().strftime('%Y%m%d%H%M%S')

        # imag
        imag = request.files['imag']
        fname = os.path.splitext(imag.filename)[1]
        basepath = os.path.dirname(__file__)
        filename = datetime.now().strftime('%Y%m%d%H%M%S')+fname
        imag.save(os.path.join(basepath, 'static/upload/images', filename))
        imag = os.path.join('upload/images', secure_filename(filename))

        # 是否上传音乐
        try:
            audio = request.files['audio']
            fname = os.path.splitext(audio.filename)[1]
            basepath = os.path.dirname(__file__)
            filename = datetime.now().strftime('%Y%m%d%H%M%S')+fname
            audio.save(os.path.join(basepath, 'static/upload/audio', filename))
            audio = os.path.join('upload/audio', secure_filename(filename))
            blog_type = 2
        except:
            audio = None

        blog = Blog_info(
            title=title,
            blog_markdown=blog_markdown,
            imag=imag,
            audio=audio,
            blog_type=blog_type,
            blog_timeid=blog_timeid,
            upload_time=upload_time,
            user_id=uid
        )

        db.session.add(blog)
        db.session.commit()

        blog = Blog_info.query.filter_by(blog_timeid=blog_timeid).first()
        return redirect(url_for('view',blog_id=blog.id))
    else:
        return render_template('markdown.html')


@app.route('/uploadimages', methods=['POST'])  # 图片上传处理 for edithormd
def uploadimages():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': u'文件格式异常'
        }
    else:
        fname = os.path.splitext(file.filename)[1]
        basepath = os.path.dirname(__file__)
        filename = datetime.now().strftime('%Y%m%d%H%M%S')+fname
        file.save(os.path.join(basepath, 'static/upload/images', filename))
        res = {
            'success': 1,
            'url': url_for('.image', name=filename)
        }
    return jsonify(res)


@app.route('/image/<name>')  # 编辑器显示图片处理 for editormd
def image(name):
    basepath = os.path.dirname(__file__)
    with open(os.path.join(basepath, 'static/upload/images', name), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp
