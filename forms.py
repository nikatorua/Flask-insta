from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

ALLOWED_IMAGES = ['jpg', 'jpeg', 'png', 'gif', 'webp']


class RegisterForm(FlaskForm):
    username = StringField('მომხმარებლის სახელი', validators=[
        DataRequired('სავალდებულო ველი'),
        Length(3, 80, message='3–80 სიმბოლო')
    ])
    email = StringField('ელ-ფოსტა', validators=[
        DataRequired(),
        Email('არასწორი ფორმატი')
    ])
    password = PasswordField('პაროლი', validators=[
        DataRequired(),
        Length(6, message='მინიმუმ 6 სიმბოლო')
    ])
    confirm = PasswordField('გაიმეორეთ პაროლი', validators=[
        DataRequired(),
        EqualTo('password', message='პაროლები არ ემთხვევა')
    ])
    submit = SubmitField('რეგისტრაცია')


class LoginForm(FlaskForm):
    email = StringField('ელ-ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')


class PostForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('აღწერა', validators=[DataRequired()])
    image = FileField('სურათი', validators=[FileAllowed(ALLOWED_IMAGES, 'მხოლოდ სურათები!')])
    submit = SubmitField('გამოქვეყნება')


class ProfileForm(FlaskForm):
    bio = TextAreaField('ბიო', validators=[Optional(), Length(max=500)])
    profile_pic = FileField('პროფილის ფოტო', validators=[FileAllowed(ALLOWED_IMAGES, 'მხოლოდ სურათები!')])
    submit = SubmitField('შენახვა')


class CommentForm(FlaskForm):
    content = TextAreaField('კომენტარი', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('გაგზავნა')
