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

@app.route('/')
def index():
    users = User.query.all()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=3000)