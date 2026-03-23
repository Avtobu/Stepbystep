from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.utils import validate_password_strength


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Register")

    def validate_password(self, field):
        errors = validate_password_strength(field.data)
        if errors:
            raise ValidationError(" ".join(errors))


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class ChangeEmailForm(FlaskForm):
    new_email = StringField("New Email", validators=[DataRequired(), Email()])
    submit_request = SubmitField("Send Verification Code")

    code = StringField("Verification Code", validators=[Length(min=0, max=6)])
    submit_confirm = SubmitField("Confirm New Email")


class DeckForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    submit = SubmitField("Save")


class CardForm(FlaskForm):
    question = TextAreaField("Question", validators=[DataRequired()])
    answer = TextAreaField("Answer", validators=[DataRequired()])
    submit = SubmitField("Save")
