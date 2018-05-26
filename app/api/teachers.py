from flask import g, jsonify, request
from .. import db
from ..models import User, Teacher, Comment
from . import api
import json
from ..decorators import login_required

# 添加老师
@login_required
@api.route("/teacher/", methods = ['POST'])
def add_teacher():
    token = request.headers.get('Authorization', None)
    decode_token = base64.b64decode(token_header)
    g.current_user = User.verify_auth_token(decode_token)
    u = User.query.filter_by(id = g.current_user).first()
    u_school_name = u.school

    tname = request.get_json().get("teacher_name")
    tschool = u_school_name
    research_direction = request.get_json().get("research_direction")
    photo = request.get_json().get("photo_url")
    sex = request.get_json().get("sex")
    birth = request.get_json().get("birth")

    new_teacher = Teacher(name = tname,
                          school = tschool,
                          research_direction = research_direction,
                          photo = photo,
                          sex = sex,
                          birth = birth)
    db.session.add(new_teacher)
    db.session.commit()

    return jsonify({
            "created":new_teacher.id
        })


# 评论老师
@login_required
@api.route("/teacher/<tid>/", methods = ['POST'])
def comment_teacher(tid):
    token = request.headers.get('Authorization', None)
    decode_token = base64.b64decode(token_header)
    g.current_user = User.verify_auth_token(decode_token)
    u = User.query.filter_by(id = g.current_user).first()
    t = Teacher.query.filter_by(id = tid).first()
    if u.school is not t.school:
        return jsonify({
                "msg":"school error"
            }), 403
    score =  request.get_json().get("score")
    content = request.get_json().get("content")
    teacher_id = tid
    author_id = u.id
    new_comment = Comment(
                score = score,
                content = content,
                teacher_id = teacher_id,
                author_id = author_id
            )
    
    # 计算平均分 
    comments_num = len(t.comments)
    t.score = (t.score*(comments_num-1) + score) / comments_num
     
    db.session.add(new_comment)
    db.session.add(t)
    db.session.commit()


# 获取某个学校老师列表
@api.route("/teacher/<schoolname>/page/<page_num>/", methods = ['GET'])
def get_teacher_list(schoolname, page_num):
    teachers = [ {
                    "tid":teacher.id,
                    "name":teacher.name,
                    "photo":teacher.photo,
                    "direction":teacher.research_direction,
                    "score":teacher.score
                 } for teacher in Teacher.filter_by(school = schoolnaem).all()] 
    allpages = len(teachers)/7
    
    ret_teachers = []
    if page_num*7-1 < len(teachers):
        ret_teachers = teachers[(page_num-1)*7: page_num*7]
    else:
        ret_teachers = teachers[(page_num-1)*7:]

    return jsonify({
            "allpages":allpages,
            "teachers":ret_teachers
        }),200


# 获取有关老师评论
@api.route("/teacher/<tid>/page/<page_num>/", methods = ['GET'])
def get_teacher(tid, page_num):
    teacher = Teacher.query.filter_by(id = tid).first()
    comments = teacher.comments
    allpages = len(comments)/5
    ret_comments = []
    if page_num * 5 -1 < len(comments):
        ret_comments = comments[(page_num-1)*5: page_num*5]
    else:
        ret_comments = comments[(page_num-1)*5:]
    return jsonify({
            "allpages":allpages,
            "comments":ret_comments
        }),200













