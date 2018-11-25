import os
from datetime import datetime

from flask import flash, get_flashed_messages, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# 导入数据库
from app import app
from app import db

# 主页


@app.route('/')
@app.route('/index')
def index():

    # 轮播区域
    post_bgs = [
        {
            'time': '2018-06-01',
            'author': 'Ming1',
            'title': 'titleA',
            'imag': '../static/images/home/01.jpg',  # 首页轮播图片为url,因此需要提前载入static
            'href_author': '#',  # 作者主页链接{{url_for()}}
            'href_blog': '#'  # 文章链接{{url_for()}}
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
            'imag': '../static/user_upload/images/01.jpg'
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
            'imag': '../static/user_upload/images/02.jpg'
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
            'imag': '../static/user_upload/images/03.jpeg',
            'audio': '../static/user_upload/audio/01.mp3'
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
            'imag': '../static/user_upload/images/04.jpeg',
            'audio': '../static/user_upload/audio/02.mp3'
        }
    ]

    return render_template('index.html', post_bgs=post_bgs, stand_as=stand_as, audio_as=audio_as)


@app.route('/blog/<blog_id>', methods=['GET', 'POST'])
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
            'author_imag': '../static/user_upload/images/02.jpg',
            'sign': '幸福生活每一天',
            'title': '这里有非常好吃的东西+1',
            'like': '283',
            'view': '400',
            'comment': '20',
            'imag': '../static/user_upload/images/02.jpg',
            'next_href': '#',
            'prev_href': '#',
            'next_title': '南锣鼓巷',
            'prev_title': '北京',
            'style':'format-standard'
        }

        # comment数量
        comment_number = '5'

        # 获取comment
        comments = [
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/user_upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            },
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/user_upload/images/02.jpg',
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
            'author_imag': '../static/user_upload/images/02.jpg',
            'sign': '幸福生活每一天',
            'title': '这里有非常好吃的东西+1',
            'like': '283',
            'view': '400',
            'comment': '20',
            'imag': '../static/user_upload/images/02.jpg',
            'next_href': '#',
            'prev_href': '#',
            'next_title': '南锣鼓巷',
            'prev_title': '北京',
            'audio': '../static/user_upload/audio/02.mp3',
            'style':'format-audio'
        }

        # comment数量
        comment_number = '5'

        # 获取comment
        comments = [
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/user_upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            },
            {
                'author': 'junjie',
                'text': '太好看了',
                'author_imag': '../static/user_upload/images/02.jpg',
                'comment_time': '2018-10-01 PM 7:23'
            }
        ]

        # 返回音乐页面
        return render_template('single-audio.html', blog=blog, comment_number=comment_number, comments=comments)

@app.route('/blog/upload')
def upload():
    return 1 #文章提交页面

@app.route('/author/<authorname>')
def author():
    return 1 #作者详情页面


