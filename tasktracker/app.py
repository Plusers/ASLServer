# -*- coding: utf-8 -*-

from flask import Flask, abort, render_template, request, jsonify, session, redirect
from utils import *
from db import *

app = Flask("SimpleTaskTracker")
template_dir = 'templates'

@app.route('/ind', methods=['GET'])
@authorized
def index():
    return render_template('index.html')

@app.route('/', methods=["GET"])
@not_authorized
def login():
    return render_template('login.html')
    
@app.route('/registration', methods=["GET"])
@not_authorized
def registration():
    return  render_template('reg.html')
    
@app.route('/ind_put', methods=["GET"])
@authorized
def ind_put():
    return render_template('index_put.html')

@app.route('/menu', methods=["GET"])
@authorized
def menu():
    return render_template('menu.html')

@app.route('/api/login', methods=["POST"])
@not_authorized
def api_login():
    login = request.form.get('login', None)

    password = request.form.get('password', None)
    if login is None or password is None:
        return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})
    user = authorize(login, password)
    if user.is_authorized():
        session['user_login'] = login
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})

@app.route('/logout', methods=["GET"])
@authorized
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/tasks', methods=["GET"])
@authorized
def api_tasks():
    login = session['user_login']
    return jsonify({"tasks": get_tasks(login)})

@app.route('/api/remove_task/<int:task_id>', methods=["GET"])
@authorized
def api_remove_task(task_id):
    login = session['user_login']
    remove_task(login, task_id)
    return jsonify({'status': 'ok'})

@app.route('/api/add_task', methods=["POST"])
@authorized
def api_add_task():
    login = session['user_login']
    name = request.form.get('name', None)
    author = request.form.get('author', None)
    _class = request.form.get('_class', None)
    if name is None or author is None or _class is None:
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    # task_id = add_task(login, text)
    book_id = add_book(name, author, _class)
    return jsonify({'status': 'ok', 'task_id': book_id})

@app.route('/api/new_task', methods=["POST"])
@authorized
def api_new_task():
    login = session['user_login']
    text = request.form.get('text', None)
    if text is None:
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    task_id = new_task(login, text)
    return jsonify({'status': 'ok', 'task_id': task_id})

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port=8001)
