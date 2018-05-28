from flask import g, jsonify, request
from .. import db
from ..models import User, Teacher, Comment
from . import api
import json
from ..decorators import login_required

# 添加老师
@api.route("/teacher/", methods = ['POST'])
@login_required
def add_teacher():
    token = request.headers.get('Authorization', None)
    g.current_user = User.verify_auth_token(token)
    print(g.current_user.school)
    u_school_name = g.current_user.school
    
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
        }), 201


# 评论老师
@login_required
@api.route("/teacher/<tid>/", methods = ['POST'])
def comment_teacher(tid):
    token = request.headers.get('Authorization', None)
    g.current_user = User.verify_auth_token(token)
    u = g.current_user
    t = Teacher.query.filter_by(id = tid).first()
    if not u.school == t.school:
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
    teacher_comments = Comment.query.filter_by(teacher_id=t.id).all()
    # 计算平均分 
    comments_num = len(teacher_comments)
    if comments_num == 0.0:
        comments_num += 1.0
    print(comments_num)
    print(score)
    t.score = (t.score*(comments_num-1.0) + score) / comments_num
     
    db.session.add(new_comment)
    db.session.add(t)
    db.session.commit()

    return jsonify({
            "msg":"success"
        }), 201


# 获取某个学校老师列表
@api.route("/teacher/<schoolname>/page/<int:page_num>/", methods = ['GET'])
def get_teacher_list(schoolname, page_num):
    PAGE_SIZE = 6
    teachers = [ {
                    "tid":teacher.id,
                    "name":teacher.name,
                    "photo":teacher.photo,
                    "direction":teacher.research_direction,
                    "score":teacher.score
                 } for teacher in Teacher.query.filter_by(school = schoolname).all()] 
    allpages = int(len(teachers)/PAGE_SIZE) + 1
    
    ret_teachers = []
    if page_num*PAGE_SIZE-1 < len(teachers):
        ret_teachers = teachers[(page_num-1)*PAGE_SIZE: page_num*PAGE_SIZE]
    else:
        ret_teachers = teachers[(page_num-1)*PAGE_SIZE:]

    return jsonify({
            "allpages":allpages,
            "teachers":ret_teachers
        }),200


# 获取有关老师评论
@api.route("/teacher/<int:tid>/info/page/<int:page_num>/", methods = ['GET'])
def get_teacher(tid, page_num):
    teacher = Teacher.query.filter_by(id = tid).first()
    t = {
        "tid":teacher.id,
        "name":teacher.name,
        "photo":teacher.photo,
        "direction":teacher.research_direction,
        "score":teacher.score,
        "sex":teacher.sex,
        "birth":teacher.birth,
        "school":teacher.school
    }

    comments = [{
        "score": comment.score,
        "content": comment.content
        } for comment in Comment.query.filter_by(teacher_id = tid).all()]

    allpages = int(len(comments)/5) + 1
    ret_comments = []
    if page_num * 5 -1 < len(comments):
        ret_comments = comments[(page_num-1)*5: page_num*5]
    else:
        ret_comments = comments[(page_num-1)*5:]
    return jsonify({
            "allpages":allpages,
            "teacher":t,
            "comments":ret_comments
        }),200
