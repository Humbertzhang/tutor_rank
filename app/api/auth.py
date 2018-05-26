from flask import jsonify, request
from .. import db
from ..models import User
from . import api
import json
from ..universities import universities_list, universities_auth

@api.route("/universities/", methods = ['GET'])
def get_unis():
    if request.method == 'GET':
        return jsonify(universities_list)

@api.route("/universities/schema/", methods = ['POST'])
def get_login_schema():
    if request.method == 'POST':
        uni_name = request.get_json().get('university_name')
        uni = universities_auth.get(uni_name)
        return jsonify(uni.schema)

@api.route("/register/", methods = ['POST'])
def register():
    if request.method == 'POST':
        uni_name = request.get_json().get('university_name')
        uni = universities_auth.get(uni_name)
        login_info = request.get_json().get('login_info')
        status = uni.login(login_info)
        if status:
            username = request.get_json().get('username')
            password = request.get_json().get('password')
            u = User.query.filter_by(username = username).first()
            if u:
                return jsonify({"msg":"username used"}),400
            else:
                new_user = User(
                    username = username,
                    password = password,
                    school = uni_name
                )
                
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'created': new_user.id}),201
        else:
            return jsonify({"msg":"register failed"}), 400
        

@api.route("/login/", methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({}), 403
        if user is not None and user.verify_password(password):
            token = user.generate_auth_token()
            return jsonify({
                "token": token
            }), 200