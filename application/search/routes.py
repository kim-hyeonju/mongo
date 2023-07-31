'''
from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl

from application import app
from flask import Blueprint, render_template, request, redirect, flash, url_for
from .forms import TodoForm
from application import db
from datetime import datetime

from bson import ObjectId


search = Blueprint(
    "search",
    __name__,
    template_folder="templates",
    static_folder="static"
)
'''