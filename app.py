from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import connect_db, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
# db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    return render_template("index.html")
