#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , request , jsonify, session , g, redirect , url_for , abort , render_template , flash, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/sylviegodard/Documents/rendu/Flask_D01/schema.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable = False)

db.create_all()

#use Bootstrap for the form
Bootstrap(app) 

#s'enregistrer sur le site
class LoginForm(FlaskForm):
    username = StringField('username', validators = [InputRequired(), Length(min = 2, max = 20)])
    password = PasswordField('password', validators = [InputRequired(), Length(min = 5, max = 100)])
    remember = BooleanField('remember me')


#s'inscrire dans la base de donnée
class RegisterForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email(message = 'Your Email is not valid'), Length(max = 20)])
    username = StringField('username', validators = [InputRequired(), Length(min = 2, max = 20)])
    password = PasswordField('password', validators = [InputRequired(), Length(min = 5, max = 100)])

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
        
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(id = data['id']).first()
#         except:
#             return jsonify({'message' : 'Token is invalid'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated
