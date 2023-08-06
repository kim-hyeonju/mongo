from werkzeug.datastructures import RequestCacheControl
from application import app
from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from .forms import UserForm
from application import db
from datetime import datetime
from functools import wraps

from bson import ObjectId
import bcrypt



# 관리자 권한
def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'manager_auth' in session:
            return f(*args, **kwargs)
        else:
            flash("관리자 영역")
            return redirect('bookfocusing.main')
    return wrap


# 로그인 후 요청가능
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("로그인이 필요합니다")
            return redirect('bookfocusing.main')
    return wrap


        
# 블루프린트로 페이지 관리
bookfocusing = Blueprint(
    "bookfocusing",
    __name__,
    template_folder="templates",
    static_folder="static"
)


# 메인 페이지
@bookfocusing.route("/main")
def main():
    return render_template("bookfocusing/main.html")


# 회원관리 페이지 (관리자만 가능)
@bookfocusing.route("/users")
@login_required
@manager_required
def users():
    todos = []
    for todo in db.user_info.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M%S")
        todos.append(todo)
    return render_template("bookfocusing/view_todos.html", todos=todos)


# 회원가입
@bookfocusing.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        form = UserForm(request.form)
        user = {
            "user_name": form.name.data,
            "student_ID": form.student_id.data,
            "password": form.passWord.data,
            "Manager": form.Manager.data
        }

        check_user = db.user_info.find_one({"studentID": user['student_ID']})

        if check_user is None:
            hashpass = bcrypt.hashpw(user['password'], bcrypt.gensalt())
            db.user_info.insert_one({
                "name": user['user_name'],
                "studentID": user['student_ID'],
                "PassWord": hashpass,
                "Manager": user['Manager'],
                "date_created": datetime.utcnow()
            })

            flash("successfully signed up", "success")
            return redirect(url_for("bookfocusing.main"))
        flash("You already signed up")
        return redirect(url_for("bookfocusing.signup"))
    else:
        form = UserForm()
    return render_template("bookfocusing/signup.html", form=form)


# 업데이트
@login_required
@manager_required
@bookfocusing.route("/update_todo/<id>", methods=['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = UserForm(request.form)
        user_name = form.name.data
        student_ID = form.student_id.data
        password = form.passWord.data
        Manager: form.Manager.data

        db.user_info.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": user_name,
            "studentID": student_ID,
            "PassWord": password,
            "Manager": Manager,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect(url_for("bookfocusing.users"))
    else:
        form = UserForm()

        todo = db.user_info.find_one_or_404({"_id": ObjectId(id)})
        form.name.data = todo.get("name", None)
        form.student_id.data = todo.get("studentID", None)
        form.passWord.data = todo.get("PassWord", None)
        form.Manager.data = todo.get("Manager", None)
    return render_template("bookfocusing/signup.html", form=form)

# 삭제
@bookfocusing.route("/delete_todo/<id>")
@login_required
@manager_required
def delete_todo(id):
    db.user_info.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect(url_for("bookfocusing.users"))


# 로그인 페이지
@bookfocusing.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = UserForm(request.form)
        userin = {
            "student_ID": form.student_id.data,
            "password": form.passWord.data
        }

        user_login = db.user_info.find_one({"studentID": userin['student_ID']})

        if user_login:
            if bcrypt.hashpw(userin['password'], user_login['PassWord']) == user_login['PassWord']:
                del userin['password']
                session['logged_in'] = True
                session['userin'] = userin
                if user_login['Manager'] == "True":
                    session['manager_auth'] = True
                return redirect(url_for('bookfocusing.main'))
        flash("wrong")
        return redirect(url_for("bookfocusing.login"))
    else:
        form = UserForm()
    return render_template("bookfocusing/login.html", form=form)


# 로그아웃
@bookfocusing.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('bookfocusing.main'))


