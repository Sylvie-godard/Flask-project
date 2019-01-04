#!/usr/bin/env python3
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
Bootstrap(app)


@app.route('/showAllUsers/')
def getAllUsers():
    req = requests.get('http://localhost:5000/api/user')
    res = req.json()
    users = res
    return render_template("showAllUser.html", title="Home", response = users['users'])


@app.route('/showOneUser/<id>')
def getOneUser(id):
    req = requests.get('http://localhost:5000/api/user/'+id)
    res = req.json()
    users = res
    return render_template("showOneUser.html", title="Home", response = users['user'])


@app.route('/api/user/<id>')
def delete(id):
    req = requests.delete('http://localhost:5000/api/user/'+id)
    res = req.json()
    users = res
    return redirect(url_for('getAllUsers'))


if __name__ == '__main__':
    app.run(port=3000)