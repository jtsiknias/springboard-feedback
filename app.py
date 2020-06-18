from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from werkzeug.exceptions import Unauthorized

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
            flash(f"Welcome, {user.first_name}", "success")
            session["username"] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def display_user(username):
    """Display user account info"""
    if "username" not in session:
        flash("You must be logged in to view that page.", "info")
        return redirect("/login")

    user = User.query.get(username)
    return render_template("users/show.html", user=user)


@app.route("/secret")
def secret_page():
    if "username" not in session:
        flash("You must be logged in first.", "info")
        return redirect("/login")

    return render_template("secret.html")


@app.route("/logout")
def logout_user():
    session.pop("username")
    flash("You've been successfully logged out.", "success")
    return redirect("/")


@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def update_feedback(id):
    """Edit user feedback"""
    if "username" not in session:
        flash("You must be logged in first.", "info")
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", feedback=feedback, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user and redirect to the login page."""
    if "username" not in session:
        flash("You must be logged in first.", "info")
        return redirect("/login")

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def create_feedback(username):
    """Create new feedback."""
    if "username" not in session:
        flash("You must be logged in first.", "info")
        return redirect("/login")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("/feedback/new.html", form=form)
