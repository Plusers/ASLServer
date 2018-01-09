from flask import Flask, abort, render_template, request, jsonify, session, redirect
from utils import authorized, not_authorized, authorize
import db


app = Flask("SimpleTaskTracker")
template_dir = 'templates'


@app.route('/', methods=["GET"])
@not_authorized
def login():
    return render_template('login.html')
    
@app.route('/registration', methods=["GET"])
@not_authorized
def registration():
    return  render_template('reg.html')

@app.route('/add_books', methods=['GET'])
@authorized
def add():
    return render_template('add_books.html')

@app.route('/list_of_books', methods=['GET'])
@authorized
def list():
    return render_template('list_of_books.html')

@app.route('/extradite_books', methods=["GET"])
@authorized
def extradite_books():
    return render_template('extradite_books.html')

@app.route('/menu', methods=["GET"])
@authorized
def menu():
    return render_template('menu.html')

@app.route('/logout', methods=["GET"])
@authorized
def logout():
    session.clear()
    return redirect('/')
    

@app.route('/api/login', methods=["POST"])
@not_authorized
def api_login():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    print('@@@ parsed login and password')
    if login is None or password is None:
        return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})
    user = authorize(login, password)
    print('@@@ created user object', user)
    if user.is_authorized():
        session['user_login'] = login
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})

@app.route('/api/add_user', methods=["POST"])
@not_authorized
def api_add_user():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    print('@@@ api_add_user fired')
    if login is None or password is None or confirm_password is None:
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    user_id = db.add_user(login, password, confirm_password)
    return jsonify({'status': 'ok', 'user_id': user_id})

@app.route('/api/books', methods=["GET"])
@authorized
def api_books():
    login = session['user_login']
    name = request.form.get('name', None)
    author = request.form.get('author', None)
    _class = request.form.get('_class', None)
    return jsonify({"books": db.get_books(name, author, _class)})

@app.route('/api/users', methods=["GET"])
@authorized
def api_users():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    return jsonify({"users": db.get_users(login, password, confirm_password)})

@app.route('/api/remove_book/<int:book_id>', methods=["GET"])
@authorized
def api_remove_book(book_id):
    login = session['user_login']
    db.remove_book(login, book_id)
    return jsonify({'status': 'ok'})

@app.route('/api/add_book', methods=["POST"])
@authorized
def api_add_book():
    login = session['user_login']
    name = request.form.get('name', None)
    author = request.form.get('author', None)
    _class = request.form.get('_class', None)
    if name is None or author is None or _class is None:
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    # task_id = add_task(login, text)
    book_id = db.add_book(name, author, _class)
    return jsonify({'status': 'ok', 'book_id': book_id})


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port=8001)
