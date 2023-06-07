from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign-In')

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    related_comics = StringField('Related Comics')
    related_characters = StringField('Related Characters')
    mentions = StringField('Mention a Friend')
    submit = SubmitField('Publish')

class UserSearchForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    submit = SubmitField('Search')

class CommissionForm(FlaskForm):
    name = TextAreaField('Name', validators=[DataRequired()])
    email = TextAreaField('Email', validators=[DataRequired()])
    subject = TextAreaField('Subject', validators=[DataRequired()])
    message = TextAreaField('Request', validators=[DataRequired()])
    budget = StringField('Budget', validators=[DataRequired()])
    submit = SubmitField("Send")

class ContactForm(FlaskForm):
    name = TextAreaField("Name")
    email = TextAreaField("Email")
    subject = TextAreaField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")

class CharSearchForm(FlaskForm):
    character_name = TextAreaField("Character Search")
    submit = SubmitField("Search")

class ComicSearchForm(FlaskForm):
    comic_name = TextAreaField("Comic Search")
    submit = SubmitField("Search")

