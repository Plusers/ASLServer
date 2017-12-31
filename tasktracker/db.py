# -*- coding: utf-8 -*-
import json

# ID | name | author | class

BOOKS_FILE = 'books.json'

def get_tasks(name, author, _class):
    with open('books.json') as f:
        tasks = json.load(f)
    if not name or author or _class in tasks:
        return []
    return tasks[name, author , _class]

def add_book(name, author, _class):
    with open(BOOKS_FILE) as f:
        tasks = json.load(f)

    book_id = len(tasks)
    tasks[book_id] = {
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
        json.dump(tasks, f)

    return book_id

def new_task(login, text):
    with open('tasks.json') as f:
        new_task = json.load(f)
    if not login in new_task:
        new_task[login] = []
        task_id = 1000
    else:
        if len(new_task[login]) == 0:
            task_id = 1000
        else:
            task_id = new_task[login][-1]["id"] + 1
    new_task[login].append({"id": task_id, "text": text})
    for i, task in enumerate(new_task[login]):
        if task['id'] == id:
            del new_task[login][i]
            break
    with open('tasks.json', 'w') as f:
        json.dump(new_task, f)
    return task_id

def remove_task(login, id):
    with open('tasks.json') as f:
        tasks = json.load(f)
    if not login in tasks:
        return
    for i, task in enumerate(tasks[login]):
        if task['id'] == id:
            del tasks[login][i]
            break
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
