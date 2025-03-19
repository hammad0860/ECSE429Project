from behave import given, when, then
import requests
from helperFunctions import get_todo_id_by_title, get_project_id_by_title

BASE_URL = "http://localhost:4567"


#Feature: Associate a TODO with a Project

# Normal flow: Associate a TODO with a Project
@when('the student associates the TODO "{todo_title}" with the project "{project_title}"')
def step_associate_todo_with_project(context, project_title, todo_title):

    todo_id = get_todo_id_by_title(todo_title)

    project_id = get_project_id_by_title(project_title)


    relationship_data = {"id": project_id}
    response = requests.post(
        f"{BASE_URL}/todos/{todo_id}/tasksof",
        json=relationship_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )

    assert response.status_code == 201
    context.response = response



@then('the TODO "{todo_title}" should be associated with the project "{project_title}"')
def step_verify_todo_association(context, todo_title, project_title):

    todo_id = get_todo_id_by_title(todo_title)
    
    response = requests.get(f"{BASE_URL}/todos/{todo_id}/tasksof", headers={"Accept": "application/json"})
    assert response.status_code == 200
    
    projects = response.json().get("projects", [])
    associated = any(proj.get("title") == project_title for proj in projects)
    assert associated, f"TODO '{todo_title}' is not associated with project '{project_title}'"






# Alternate flow: Associate a TODO with a different Project
@when('the student associates the TODO "{todo_title}" with a different project "{new_project}"')
def step_associate_todo_with_different_project(context, todo_title, new_project):
  
    todo_id = get_todo_id_by_title(todo_title)

    project_id = get_project_id_by_title(new_project)



    relationship_data = {"id": project_id}
    response = requests.post(
        f"{BASE_URL}/todos/{todo_id}/tasksof",
        json=relationship_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 201
    context.response = response


@then('the TODO "{todo_title}" should be associated with both projects "{original_project}" and "{new_project}"')
def step_verify_todo_association_multiple(context, todo_title, original_project, new_project):

    todo_id = get_todo_id_by_title(todo_title)

    response = requests.get(f"{BASE_URL}/todos/{todo_id}/tasksof", headers={"Accept": "application/json"})
    assert response.status_code == 200
    projects_data = response.json().get("projects", [])
    
    original_project_id = get_project_id_by_title(original_project)
    new_project_id = get_project_id_by_title(new_project)
    
    associated_ids = [proj.get("id") for proj in projects_data]
    
    assert original_project_id in associated_ids
    assert new_project_id in associated_ids

@then("the student is notified that the association operation was successful")
def step_verify_association_success(context):
    assert context.response.status_code == 201




# Error Flow: Associate a TODO with a non-existent Project
@when('the student attempts to associate the TODO with id "{id}" with the project "{project_title}"')
def step_attempt_associate_todo_by_id(context, id, project_title):

    project_id = get_project_id_by_title(project_title)
    
    relationship_data = {"id": project_id}
    
    response = requests.post(
        f"{BASE_URL}/todos/{id}/tasksof",
        json=relationship_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    
    context.response = response



