# -*- coding: utf-8 -*-
import json

# ID | name | author | class

BOOKS_FILE = 'books.json'

def get_books(name, author, _class):
    with open('books.json') as f:
        books = json.load(f)
    if not name or author or _class in books:
        return []
    return books[name, author , _class]

def add_book(name, author, _class):
    with open(BOOKS_FILE) as f:
        books = json.load(f)

    book_id = len(books)
    books[book_id] = {
        'name': name,
        'author': author,
        'class': _class,
    }
    # if not login in tasks:
    #     tasks[login] = []
    #     task_id = 1
    # else:
    #     if len(tasks[login]) == 0:
    #         task_id = 1
    #     else:
    #         task_id = tasks[login][-1]["id"] + 1
    # tasks[login].append({"id": task_id, "text": text})

    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f)

    return book_id

def remove_book(login, id):
    with open('books.json') as f:
        books = json.load(f)
    if not login in books:
        return
    for i, book in enumerate(books[login]):
        if book['id'] == id:
            del books[login][i]
            break
    with open('books.json', 'w') as f:
        json.dump(books, f)
