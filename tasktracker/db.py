# -*- coding: utf-8 -*-
import json

def get_tasks(login):
    with open('tasks.json') as f:
        tasks = json.load(f)
    if not login in tasks:
        return []
    return tasks[login]

def add_task(login, text):
    with open('tasks.json') as f:
        tasks = json.load(f)
    if not login in tasks:
        tasks[login] = []
        task_id = 1
    else:
        if len(tasks[login]) == 0:
            task_id = 1
        else:
            task_id = tasks[login][-1]["id"] + 1
    tasks[login].append({"id": task_id, "text": text})
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    return task_id
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
