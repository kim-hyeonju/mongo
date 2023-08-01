from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl

from application import app
from flask import Blueprint, render_template, request, redirect, flash, url_for
from .forms import UserForm
from application import db
from datetime import datetime

from bson import ObjectId


bookfocusing = Blueprint(
    "bookfocusing",
    __name__,
    template_folder="templates",
    static_folder="static"
)


# 메인 페이지, 로그인, 회원가입 버튼
@bookfocusing.route("/main")
def main():
    return render_template("bookfocusing/layout.html")


@bookfocusing.route("/users")
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
        user_name = form.name.data
        student_ID = form.student_id.data
        password = form.passWord.data

        db.user_info.insert_one({
            "name": user_name,
            "studentID": student_ID,
            "PassWord": password,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")
        return redirect(url_for("bookfocusing.get_todo"))
    else:
        form = UserForm()
    return render_template("bookfocusing/signup.html", form=form)


@bookfocusing.route("/update_todo/<id>", methods=['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = UserForm(request.form)
        user_name = form.name.data
        student_ID = form.student_id.data
        password = form.passWord.data

        db.user_info.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": user_name,
            "studentID": student_ID,
            "PassWord": password,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect(url_for("bookfocusing.get_todo"))
    else:
        form = UserForm()

        todo = db.user_info.find_one_or_404({"_id": ObjectId(id)})
        form.name.data = todo.get("name", None)
        form.student_id.data = todo.get("studentID", None)
        form.passWord.data = todo.get("PassWord", None)
    return render_template("bookfocusing/signup.html", form=form)


@bookfocusing.route("/delete_todo/<id>")
def delete_todo(id):
    db.user_info.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect(url_for("bookfocusing.get_todo"))
