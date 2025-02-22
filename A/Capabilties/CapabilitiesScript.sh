#!/bin/bash

# Base URL for API endpoints
BASE_URL="http://localhost:4567"

echo "Testing TODOS endpoints"

# 1. GET all todos
echo "GET /todos"
curl -s -X GET "$BASE_URL/todos" -H "Accept: application/json"
echo -e "\n-------------------------"

# 2. POST create a new todo (no ID required)
echo "POST /todos (create new todo)"
curl -s -X POST "$BASE_URL/todos" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Test Todo", "doneStatus": "false", "description": "A test todo item"}'
echo -e "\n-------------------------"

# 3. GET a specific todo (assuming id "1" exists)
echo "GET /todos/1"
curl -s -X GET "$BASE_URL/todos/1" -H "Accept: application/json"
echo -e "\n-------------------------"

# 4. PUT update todo with id=1
echo "PUT /todos/1 (update todo)"
curl -s -X PUT "$BASE_URL/todos/1" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Updated Todo", "doneStatus": "true", "description": "Updated description"}'
echo -e "\n-------------------------"

# 5. DELETE todo with id=1
echo "DELETE /todos/1"
curl -s -X DELETE "$BASE_URL/todos/1"
echo -e "\n-------------------------"

# Relationship endpoints for todos
echo "=== Testing TODO relationships ==="

# GET categories related to todo (assuming todo with id=2 exists)
echo "GET /todos/2/categories"
curl -s -X GET "$BASE_URL/todos/2/categories" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between todo id=2 and category id=99
echo "POST /todos/2/categories (associate category id=99)"
curl -s -X POST "$BASE_URL/todos/2/categories" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "99"}'
echo -e "\n-------------------------"

# DELETE relationship between todo id=2 and category id=99
echo "DELETE /todos/2/categories/99"
curl -s -X DELETE "$BASE_URL/todos/2/categories/99"
echo -e "\n-------------------------"

# GET projects related to todo (relationship named tasksof)
echo "GET /todos/2/tasksof"
curl -s -X GET "$BASE_URL/todos/2/tasksof" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between todo id=2 and project id=99
echo "POST /todos/2/tasksof (associate project id=99)"
curl -s -X POST "$BASE_URL/todos/2/tasksof" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "99"}'
echo -e "\n-------------------------"

# DELETE relationship between todo id=2 and project id=99
echo "DELETE /todos/2/tasksof/99"
curl -s -X DELETE "$BASE_URL/todos/2/tasksof/99"
echo -e "\n========================="

echo "=== Testing PROJECT endpoints ==="

# 1. GET all projects
echo "GET /projects"
curl -s -X GET "$BASE_URL/projects" -H "Accept: application/json"
echo -e "\n-------------------------"

# 2. POST create a new project
echo "POST /projects (create new project)"
curl -s -X POST "$BASE_URL/projects" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Test Project", "completed": "false", "active": "true", "description": "A test project"}'
echo -e "\n-------------------------"

# 3. GET a specific project (assuming id "99" exists)
echo "GET /projects/99"
curl -s -X GET "$BASE_URL/projects/99" -H "Accept: application/json"
echo -e "\n-------------------------"

# 4. PUT update project with id=99
echo "PUT /projects/99 (update project)"
curl -s -X PUT "$BASE_URL/projects/99" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Updated Project", "completed": "true", "active": "false", "description": "Updated description"}'
echo -e "\n-------------------------"

# 5. DELETE project with id=99
echo "DELETE /projects/99"
curl -s -X DELETE "$BASE_URL/projects/99"
echo -e "\n-------------------------"

# Relationship endpoints for projects
echo "=== Testing PROJECT relationships ==="

# GET tasks (todos) related to project id=2
echo "GET /projects/2/tasks"
curl -s -X GET "$BASE_URL/projects/2/tasks" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between project id=2 and todo id=5
echo "POST /projects/2/tasks (associate todo id=5)"
curl -s -X POST "$BASE_URL/projects/2/tasks" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "5"}'
echo -e "\n-------------------------"

# DELETE relationship between project id=2 and todo id=5
echo "DELETE /projects/2/tasks/5"
curl -s -X DELETE "$BASE_URL/projects/2/tasks/5"
echo -e "\n-------------------------"

# GET categories related to project id=2
echo "GET /projects/2/categories"
curl -s -X GET "$BASE_URL/projects/2/categories" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between project id=2 and category id=99
echo "POST /projects/2/categories (associate category id=99)"
curl -s -X POST "$BASE_URL/projects/2/categories" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "99"}'
echo -e "\n-------------------------"

# DELETE relationship between project id=2 and category id=99
echo "DELETE /projects/2/categories/99"
curl -s -X DELETE "$BASE_URL/projects/2/categories/99"
echo -e "\n========================="

echo "=== Testing CATEGORY endpoints ==="

# 1. GET all categories
echo "GET /categories"
curl -s -X GET "$BASE_URL/categories" -H "Accept: application/json"
echo -e "\n-------------------------"

# 2. POST create a new category
echo "POST /categories (create new category)"
curl -s -X POST "$BASE_URL/categories" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Test Category", "description": "A test category"}'
echo -e "\n-------------------------"

# 3. GET a specific category (assuming id "99" exists)
echo "GET /categories/99"
curl -s -X GET "$BASE_URL/categories/99" -H "Accept: application/json"
echo -e "\n-------------------------"

# 4. PUT update category with id=99
echo "PUT /categories/99 (update category)"
curl -s -X PUT "$BASE_URL/categories/99" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title": "Updated Category", "description": "Updated description"}'
echo -e "\n-------------------------"

# 5. DELETE category with id=99
echo "DELETE /categories/99"
curl -s -X DELETE "$BASE_URL/categories/99"
echo -e "\n-------------------------"

# Relationship endpoints for categories
echo "=== Testing CATEGORY relationships ==="

# GET todos related to category id=2
echo "GET /categories/2/todos"
curl -s -X GET "$BASE_URL/categories/2/todos" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between category id=2 and todo id=5
echo "POST /categories/2/todos (associate todo id=5)"
curl -s -X POST "$BASE_URL/categories/2/todos" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "5"}'
echo -e "\n-------------------------"

# DELETE relationship between category id=2 and todo id=5
echo "DELETE /categories/2/todos/5"
curl -s -X DELETE "$BASE_URL/categories/2/todos/5"
echo -e "\n-------------------------"

# GET projects related to category id=2
echo "GET /categories/2/projects"
curl -s -X GET "$BASE_URL/categories/2/projects" -H "Accept: application/json"
echo -e "\n-------------------------"

# POST create relationship between category id=2 and project id=99
echo "POST /categories/2/projects (associate project id=99)"
curl -s -X POST "$BASE_URL/categories/2/projects" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"id": "99"}'
echo -e "\n-------------------------"

# DELETE relationship between category id=2 and project id=99
echo "DELETE /categories/2/projects/99"
curl -s -X DELETE "$BASE_URL/categories/2/projects/99"
echo -e "\n========================="

echo "=== Fetching Documentation and Shutting Down Server ==="

# GET the API docs (HTML)
echo "GET /docs (API documentation)"
curl -s -X GET "$BASE_URL/docs"
echo -e "\n-------------------------"

# GET /shutdown to stop the server 
echo "GET /shutdown (shutting down the API server)"
curl -s -X GET "$BASE_URL/shutdown"
echo -e "\n========================="

echo "API test script completed."
