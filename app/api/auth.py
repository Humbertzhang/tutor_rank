from flask import jsonify, request, make_response, session
from .. import db
from ..models import User
from . import api
import json
from ..universities import universities_list, universities_auth, universities_engname, universities_verify
import base64

# 大学列表
@api.route("/universities/", methods = ['GET'])
def get_unis():
    if request.method == 'GET':
        return jsonify({"universities":universities_list})


# 该学校所需登录验证方式
@api.route("/universities/schema/", methods = ['POST'])
def get_login_schema():
    if request.method == 'POST':
        uni_name = request.get_json().get('university_name')
        uni = universities_auth.get(uni_name)
        return jsonify(uni.schema)

@api.route("/universities/pre_verify/", methods = ['POST'])
def pre_verify():
    if request.method == 'POST':
        uni = request.get_json().get('university_name')
        university_class = universities_auth.get(uni)
        if university_class.schema.get("verify") == 1:
            verify_func = universities_verify.get(uni)
            pic = verify_func(None)
            print("PRE:", request.remote_addr)
            session[str(request.remote_addr)] = pic 
            return jsonify({"msg":"ok"})
       

# 验证码
@api.route("/universities/verify/", methods = ['POST'])
def get_verify_code():
    if request.method == 'POST':
        print("AFTER:", request.remote_addr)
        pic = session[str(request.remote_addr)]

        response = make_response(pic)
        response.headers.set('Content-Type', 'image/jpeg')
        return response

# 登录
@api.route("/login/", methods = ['POST'])
def login():
    if request.method == 'POST':
        uni = request.get_json().get('university_name')
        login_info =  request.get_json().get('login_info')
        username = uni + login_info.get('username')
        password = login_info.get('password')
        
        user = User.query.filter_by(username=username).first()
        # register
        if not user:
            # 通过了验证 
            if universities_auth.get(uni).login(None, login_info):
                new_user = User(
                                username = username,
                                password = password,
                                school = universities_engname.get(uni)
                           )
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(username=username).first()
                token = user.generate_auth_token().decode("utf-8") 
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
                token = user.generate_auth_token().decode("utf-8")
                return jsonify({
                    "token": token
                }), 200
        else:
            return jsonify({"msg":"failed"}), 401

