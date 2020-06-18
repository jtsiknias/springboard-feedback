from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(
            message="Username cannot be blank."),
            Length(max=20, message="Username cannot be more than 20 characters long.")])

    password = PasswordField(
        "Password",
        validators=[InputRequired(
            message="Password cannot be blank.")])

    email = StringField(
        "Email",
        validators=[InputRequired(
            message="Email cannot be blank."),
            Email(),
            Length(max=50, message="Email cannot be more than 50 characters long.")])

    first_name = StringField(
        "First Name",
        validators=[InputRequired(
            message="First name cannot be blank."),
            Length(max=30, message="First name cannot be more than 30 characters long.")])

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(
            message="Last name cannot be blank."),
            Length(max=30, message="Last name cannot be more than 30 characters long.")])


class LoginForm(FlaskForm):
    """User login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(
            message="Username cannot be blank."),
            Length(max=20, message="Username cannot be more than 20 characters long.")])

    password = PasswordField(
        "Password",
        validators=[InputRequired(
            message="Password cannot be blank.")])


class FeedbackForm(FlaskForm):
    """Add new feedback."""
    title = StringField("Title",
                        validators=[InputRequired(message="Title cannot be blank."),
                                    Length(max=100, message="Title length cannot be more than 100 characters.")])

    content = StringField("Content",
                          validators=[InputRequired(message="Content cannot be blank.")])
