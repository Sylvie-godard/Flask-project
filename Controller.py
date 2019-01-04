#!/usr/bin/env python3

from Model import *
import uuid
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    users = User.query.all()
    return render_template("index.html", title="Home", users = users)

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user created ! </h1>'
    return render_template('register.html', form = form)


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('index'))

        return '<h1> Invalid username or password</h1>'
    return render_template('login.html', form = form)


@app.route('/api/user/', methods = ['GET'])
# @token_required
def getAllUsers():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users' :  output })


@app.route('/api/user/<id>', methods = ['GET'])
# @token_required
def getOneUser(id):
    user = User.query.filter_by(id = id).first()

    if not user: 
        return jsonify({'message' : 'No user found'})
    user_data = {}
    user_data['username'] = user.username
    user_data['id'] = user.id
    user_data['public_id'] = user.public_id
    user_data['email'] = user.email
    user_data['password'] = user.password
    return jsonify({'user' : user_data})


@app.route('/api/user/', methods = ['POST'])
# @token_required
def createUser():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method = 'sha256')

    new_user = User(public_id = str(uuid.uuid4()) ,username = data['username'], email = data['email'], password = hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'}), 201


@app.route('/api/user/<id>', methods = ['PUT'])
# @token_required
def updateUser(id):
    data = request.get_json()
    user = User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()

    return jsonify({'message' : 'User updated'})

@app.route('/api/user/<id>', methods = ['DELETE'])
# @token_required
def delete(id):
    user = User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})


@app.route('/api/login/')
# @token_required
def loginapi():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required !"'})
    user = User.query.filter_by(username = auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required!"'})


if __name__ == '__main__':
    app.run(debug = True)
