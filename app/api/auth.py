from flask import jsonify, request
from .. import db
from ..models import User
from . import api
import json
from ..universities import universities_list, universities_auth


# 大学列表
@api.route("/universities/", methods = ['GET'])
def get_unis():
    if request.method == 'GET':
        return jsonify(universities_list)


# 该学校所需登录验证方式
@api.route("/universities/schema/", methods = ['POST'])
def get_login_schema():
    if request.method == 'POST':
        uni_name = request.get_json().get('university_name')
        uni = universities_auth.get(uni_name)
        return jsonify(uni.schema)

# 登录
@api.route("/login/", methods = ['POST'])
def login():
    if request.method == 'POST':
        uni = request.get_json().get('university_name')
        login_info =  request.get_json().get('login_info')
        username = uni + login_info.get('sid')
        password = request.get_json().get('password')
        user = User.query.filter_by(username=username).first()
        # register
        if not user:
            # 通过了验证 
            if universities_auth.get(uni).login(login_info):
                new_user = User(
                                username = username,
                                password = password,
                                school = uni
                           )
                db.session.add(new_user)
                db.session.commit()
                token = user.generate_auth_token()
                return jsonify({    
                                'created': new_user.id,
                                'token': token
                                }),201
            # 未通过验证
            return jsonify({
                    "msg":"school check failed"
                }), 401

        # login
        elif user.verify_password(password):
                token = user.generate_auth_token()
                return jsonify({
                    "token": token
                }), 200
        else:
            return jsonify({"msg":"failed"}), 401

