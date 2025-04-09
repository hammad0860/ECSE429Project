import requests

BASE_URL = "http://localhost:4567/todos"

def createTodo(data):
    return requests.post(BASE_URL, json=data)

def updateTodo(todo_id, data):
    return requests.post(f"{BASE_URL}/{todo_id}", json=data)

def deleteTodo(todo_id):
    return requests.delete(f"{BASE_URL}/{todo_id}")
