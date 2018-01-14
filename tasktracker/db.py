import json


BOOKS_FILE = 'books.json'
USERS_FILE = 'users.json'


def get_books(login):
    with open('books.json') as f:
        books = json.load(f)
    return books[login]

def add_book(login, name, author, _class):
    with open(BOOKS_FILE) as f:
        books = json.load(f)
    
    books[login] = {
        'name': name,
        'author': author,
        'class': _class,
    }

    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f)

    return login

def get_users(login, password, confirm_password, profile):
    with open(USERS_FILE) as f:
        users = json.load(f)
    if not login or password or confirm_password or profile in users:
        return []
    return users[login, password , confirm_password, profile]

def add_user(login, password, confirm_password, profile):
    with open(USERS_FILE) as f:
        users = json.load(f)

    user_id = len(users)
    users[login] = {
        'password': password,
        'profile': profile,
    }

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

    return user_id

def remove_book(login, id):
    with open(BOOKS_FILE) as f:
        books = json.load(f)
    if not login in books:
        return
    for i, book in enumerate(books[login]):
        if book['id'] == id:
            del books[login][i]
            break
    with open('books.json', 'w') as f:
        json.dump(books, f)
