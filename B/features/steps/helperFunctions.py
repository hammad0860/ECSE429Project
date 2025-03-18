import requests
BASE_URL = "http://localhost:4567"

    
def get_todo_id_by_title(title):
 
    response = requests.get(f"{BASE_URL}/todos", headers={"Accept": "application/json"})

    todos = response.json().get("todos", [])
    
    for todo in todos:
        if todo["title"] == title:
            return todo["id"]
    
    return None


def get_project_id_by_title(title):
    response = requests.get(f"{BASE_URL}/projects", headers={"Accept": "application/json"})

    projects = response.json().get("projects", [])
    
    for project in projects:
        if project["title"] == title:
            return project["id"]
    return None

