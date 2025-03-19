from behave import given, when, then
import requests 
from distutils.util import strtobool
from helperFunctions import get_todo_id_by_title

BASE_URL = "http://localhost:4567"

# Feature: Create a New TODO

# Normal Flow: Creating a New TODO with Title and Description

@when('the student creates a new TODO with todo_title "{todo_title}" and description "{description}"')
def step_create_todo_generic(context, todo_title, description):

    payload = {
        "title": todo_title,
        "description": description,
        "doneStatus": False
    }
    response = requests.post(
        f"{BASE_URL}/todos",
        json=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    context.response = response

@then('a new TODO with todo_title "{todo_title}" should exist with doneStatus "false" and description "{description}"')
def step_verify_todo_created(context, todo_title, description):

    response = requests.get(f"{BASE_URL}/todos", headers={"Accept": "application/json"})
    todos = response.json().get("todos", [])
    found = any(todo.get("title") == todo_title and 
                todo.get("description") == description and 
                todo.get("doneStatus") == "false" for todo in todos)
    
    assert found

@then("the student is notified that the creation operation was successful")
def step_verify_creation_success(context):
    assert context.response.status_code == 201


# Alternative Flow: Creating a New TODO with Title Only

@when('the student creates a new TODO with todo_title "{todo_title}" and no description')
def step_create_todo_with_title_only(context, todo_title):

    payload = {
        "title": todo_title,
        "description": ""
    }

    response = requests.post(
        f"{BASE_URL}/todos",
        json=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )

    context.response = response

@then('a new TODO with todo_title "{todo_title}" should exist with doneStatus "false" and an empty description')
def step_verify_todo_created_with_empty_desc(context, todo_title):

    response = requests.get(f"{BASE_URL}/todos", headers={"Accept": "application/json"})
    
    todos = response.json().get("todos", [])
    found = any(todo.get("title") == todo_title and 
                todo.get("description") == "" and 
                todo.get("doneStatus") == "false" for todo in todos)
    
    assert found

# Error Flow: Creating a New TODO with an Invalid doneStatus

@when('the student creates a new TODO with todo_title "{todo_title}", description "{description}" and doneStatus "{doneStatus}"')
def step_create_todo_with_invalid_doneStatus(context, todo_title, description, doneStatus):
    payload = {
        "title": todo_title,
        "description": description,
        "doneStatus": doneStatus  
    }
    response = requests.post(
        f"{BASE_URL}/todos",
        json=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    
    context.response = response


@then('the system should notify the student with the error message "{message}"')
def step_verify_error_message(context, message):
 
    assert context.response.status_code  == 400 
    error_data = context.response.json()

    error_message = error_data.get("errorMessages")[0]
    
    
    assert message == error_message






