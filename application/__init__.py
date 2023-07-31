

from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["SECRET_KEY"] = "81185101eb0ebc8a409352fd778528e2ac355daa"
app.config["MONGO_URI"] = "mongodb+srv://KimHY:rlaguswn12@kimhyeonju.o9b3ukl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# setup mongodb
mongodb_clinet = PyMongo(app)
db = mongodb_clinet.db

from application.bookfocusing import routes as bookfocus_route
app.register_blueprint(bookfocus_route.bookfocusing, url_prefix="/bookfocusing")
