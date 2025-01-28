from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed , FileField
from wtforms import StringField , PasswordField , SubmitField  
from wtforms.validators import  Regexp , DataRequired , Length , ValidationError
from flask_ckeditor import CKEditorField
from db import db



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z][A-Za-z0-9]{4,18}$', message='Username must be 5-19 characters long and start with a letter.')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d|.*\W)(?!.*[.\n]).{8,}$',
            message='Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number or special character.'
        )
    ])
    submit = SubmitField('Login')


class SignForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z][A-Za-z0-9]{4,18}$',
               message='Username must be 5-19 characters long and start with a letter.')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d|.*\W)(?!.*[.\n]).{8,}$',
            message='Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number or special character.'
        )
    ])
    submit = SubmitField('Sign up')


class AddArticles(FlaskForm):
    article_name = StringField(label='Article Name' , validators=[DataRequired() , Length(min=2 , max=25)])
    article_bio = CKEditorField(label='Article Bio', validators=[
                                DataRequired(), Length(min=25)])
    article_img = FileField(label='Article Image' , validators=[DataRequired() , FileAllowed(['png' , 'jpg' , 'jpeg'])])
    add_Article_btn = SubmitField(label='Add Article')


class updateAccount(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(), Regexp(
        r'^[A-Za-z][A-Za-z0-9]{4,18}$', message='Username must be 5-19 characters long and start with a letter.')])
    password = StringField(label='password', validators=[Regexp(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d|.*\W)(?!.*[.\n]).{8,}$',
        message='Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number or special character.'
    ) , DataRequired()])
    userImage = FileField(label='image' , validators=[FileAllowed(['png' , 'jpg' , 'jpeg'])])
    submitBtn = SubmitField(label = 'update Account')


class updateArticle(FlaskForm):
    article_name = StringField(label='Article Name', validators=[DataRequired()])

    article_bio = CKEditorField(label='Article Bio', validators=[
                                DataRequired(), Length(min=25)])
    article_img = FileField(label='Article Image', validators=[
                            DataRequired(), FileAllowed(['png', 'jpg', 'jpeg'])])

    submitBtn = SubmitField(label='update Article')
