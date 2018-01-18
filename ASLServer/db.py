import json
import qrcode

BOOKS_FILE = 'books.json'
USERS_FILE = 'users.json'


def get_books(login):
    with open('books.json') as f:
        books = json.load(f)
    if not login in books:
        return []
    return books[login]

def add_book(login, name, author, _class, numIzd, nameIzd):
    with open(BOOKS_FILE) as f:
        books = json.load(f)
    book_id = len(books)
    books[book_id] = {
        'name': name,
        'author': author,
        'class': _class,
        'numIzd': numIzd,
        'nameIzd': nameIzd,
    }
    img = qrcode.make(login + "/" + name + "/" + author + "/" + _class +"/"+numIzd+"/"+nameIzd)
    img.save("/home/vladislav/Документы/ASLServer/ASLServer/qr-books/"+login+".png")
    img.show()
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f)

    return login

def get_users(login, name,  surname, third_name, password, confirm_password, profile):
    with open(USERS_FILE) as f:
        users = json.load(f)
    if not login or name or surname  or third_name or password or confirm_password or profile in users:
        return []
    return users[login, name, surname, third_name, password , confirm_password, profile]

def add_user(login,name, surname, third_name, password, confirm_password, profile):
    with open(USERS_FILE) as f:
        users = json.load(f)

    user_id = len(users)
    users[login] = {
        'name': name,
        'surname': surname, 
        'third_name': third_name,    
        'password': password,
        'profile': profile,
    }
    img = qrcode.make(login + " " + name + " " + surname + " " + third_name +" "+password+" "+profile)
    img.save("/home/vladislav/Документы/ASLServer/ASLServer/qr-users/"+name+surname+third_name+".png")
    img.show()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

    return user_id

