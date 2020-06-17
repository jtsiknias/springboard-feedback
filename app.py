from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

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
    """Simply redirects user to /register page"""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        flash("Account has been created. Welcome!", "success")
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.first_name}", "success")
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


@app.route("/secret")
def secret_page():
    return render_template("secret.html")
