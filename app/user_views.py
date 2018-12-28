import os
import re
from io import BytesIO

from flask import Blueprint, render_template, make_response, session, jsonify, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from utils import status_code
from utils.code import Captcha
from utils.functions import login_status
from utils.settings import MEDIA_PATH

blue_user = Blueprint('user', __name__)


@blue_user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@blue_user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@blue_user.route('/my/', methods=['GET'])
@login_status
def my():
    return render_template('my.html')


@blue_user.route('/profile/', methods=['GET'])
@login_status
def profile():
    return render_template('profile.html')


@blue_user.route('/auth/', methods=['GET'])
@login_status
def auth():
    return render_template('auth.html')


@blue_user.route('/get_code/')
def get_code():
    text, image = Captcha.gen_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'

    session['code'] = text
    return resp


@blue_user.route('/register/', methods=['POST'])
def register1():
    mobile = request.form.get('mobile')
    image_code = request.form.get('imagecode')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    session_code = session.get('code')
    if not all([mobile, image_code, password, password2]):
        return jsonify(status_code.REGISTER_ERROR_INFO_IS_NULL)
    if not image_code == session_code:
        return jsonify(status_code.REGISTER_ERROR_CODE_ERROR)
    if not password == password2:
        return jsonify(status_code.REGISTER_ERROR_PASSWORD_DIFFER)
    user = User.query.filter(User.phone == mobile).first()
    if user:
        return jsonify(status_code.REGISTER_ERROR_USER_IS_EXIST)
    user = User()
    user.phone = mobile
    user.password = password
    user.add_update()
    return jsonify(status_code.SUCCESS)


@blue_user.route('/login/', methods=['POST'])
def login1():
    username = request.form.get('username')
    password = request.form.get('password')
    if not all([username, password]):
        return jsonify(status_code.LOGIN_ERROR_INFO_IS_NULL)
    user = User.query.filter(User.phone == username).first()
    if not user:
        return jsonify(status_code.LOGIN_ERROR_USER_OR_PASSWORD_ERROR)
    if not user.check_pwd(password):
        return jsonify(status_code.LOGIN_ERROR_USER_OR_PASSWORD_ERROR)
    session['user_id'] = user.id
    return jsonify(status_code.SUCCESS)


@blue_user.route('/logout/', methods=['GET'])
@login_status
def logout():
    session.pop('user_id')
    return jsonify(status_code.SUCCESS)


@blue_user.route('/my_info/', methods=['GET'])
@login_status
def my_info():
    id = session.get('user_id')
    user = User.query.filter(User.id == id).first()
    data = {
        'phone': user.phone,
        'name': user.name,
        'avatar': user.avatar
    }
    return jsonify(data)


@blue_user.route('/get_profile/', methods=['GET'])
@login_status
def get_profile():
    id = session['user_id']
    user = User.query.filter(User.id == id).first()
    return jsonify(user.to_basic_dict())


@blue_user.route('/add_update_avatar/', methods=['PATCH'])
@login_status
def avatar():
    # 1获取图片
    avatar = request.files.get('avatar')
    # 保存图片
    path = os.path.join(MEDIA_PATH, avatar.filename)
    avatar.save(path)
    # 修改字段
    user = User.query.filter(User.id == session['user_id']).first()
    user.avatar = avatar.filename
    user.add_update()
    return jsonify(status_code.SUCCESS)


@blue_user.route('/update_name/', methods=['POST'])
@login_status
def update_name():
    name = request.form.get('name')
    user = User.query.filter(User.id == session['user_id']).first()
    if name == user.name:
        return jsonify(status_code.UPDATE_NAME_ERROR_IS_EXIST)
    user.name = name
    user.add_update()
    return jsonify(status_code.SUCCESS)


@blue_user.route('/get_auth/', methods=['GET'])
@login_status
def get_auth():
    user = User.query.filter(User.id == session['user_id']).first()
    id_name = user.id_name
    if id_name:
        data = {
            'code': 1008,
            'real_name': user.id_name,
            'id_card': user.id_card
        }
        return jsonify(data)
    return jsonify(status_code.AUTH_STATUS_NOT_AUTH)


@blue_user.route('/auth/', methods=['POST'])
@login_status
def auth1():
    user = User.query.filter(User.id == session['user_id']).first()
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    re_str = r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)'
    if not all([real_name, id_card]):
        return jsonify(status_code.AUTH_ERROR_INFO_IS_NULL)
    if not re.match(re_str, id_card):
        return jsonify(status_code.AUTH_ERROR_ID_CARD_ERROR)
    user.id_name = real_name
    user.id_card = id_card
    user.add_update()
    return jsonify(status_code.SUCCESS)

















