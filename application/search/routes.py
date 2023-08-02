from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl

from application import app
from flask import Blueprint, render_template, request, redirect, flash, url_for
from .forms import BookForm
from application import db
from datetime import datetime

from bson import ObjectId
from bson.json_util import dumps


search = Blueprint(
    "search",
    __name__,
    template_folder="templates",
    static_folder="static"
)


# book db 
@search.route("/management")
def management():
    todos = []
    for todo in db.book_info.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M%S")
        todos.append(todo)
    return render_template("search/manage.html", todos=todos)


# 책 추가입력 creat
@search.route("/add_book", methods=["POST", "GET"])
def add_book():
    if request.method == "POST":                # 입력받기
        form = BookForm(request.form)
        book_title = form.title.data
        book_shelf = form.shelf.data
        book_block = form.block.data
        book_writer = form.writer.data
        book_loan = form.loan.data

        db.book_info.insert_one({               # MongoDB에 insert
            "title": book_title,
            "shelf": book_shelf,
            "block": book_block,
            "writer": book_writer,
            "loan": book_loan,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")         # 성공했다는 flask창
        return redirect(url_for("search.management"))
    else:
        form = BookForm()
    return render_template("search/crud_book.html", form=form)


# book db update
@search.route("/update_book/<id>", methods=['POST', 'GET'])
def update_book(id):
    if request.method == "POST":
        form = BookForm(request.form)
        book_title = form.title.data
        book_shelf = form.shelf.data
        book_block = form.block.data
        book_writer = form.writer.data
        book_loan = form.loan.data

        db.book_info.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "title": book_title,
            "shelf": book_shelf,
            "block": book_block,
            "writer": book_writer,
            "loan": book_loan,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect(url_for("search.management"))
    else:
        form = BookForm()

        search = db.book_info.find_one_or_404({"_id": ObjectId(id)})
        form.title.data = search.get("title", None)
        form.shelf.data = search.get("shelf", None)
        form.block.data = search.get("block", None)
        form.writer.data = search.get("writer", None)
        form.loan.data = search.get("loan", None)
    return render_template("search/crud_book.html", form=form)


# book db delete
@search.route("/delete_book/<id>")
def delete_book(id):
    db.book_info.find_one_and_delete({"_id": ObjectId(id)})
    return redirect(url_for("search.management"))


@search.route("/books", methods=["POST", "GET"])
def books():
    if request.method == 'POST':
        form = BookForm(request.form)
        needbook = form.title.data
        # db.book_info.find_one({"title": txt})
        return redirect(url_for("search.book", needbook=needbook))
    else:
        form = BookForm()
    return render_template("search/please.html", form=form)


@search.route("/book/<needbook>")
def book(needbook):
    needs = db.book_info.find({"title": needbook}).limit(10)
    return render_template("search/list.html", needs=needs)
