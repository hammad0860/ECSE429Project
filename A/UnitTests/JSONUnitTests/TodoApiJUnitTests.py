import unittest
import subprocess
import requests
import json
import time
import os
from deepdiff import DeepDiff



BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
APPLICATION_RUNNING = False
WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
APPLICATION_PROCESS = None




class TodoApiUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.expected_json_all_ids = {
                "todos": [
                    {
                        "id": "1",
                        "title": "scan paperwork",
                        "doneStatus": "false",
                        "description": "",
                        "categories": [{"id": "1"}],
                        "tasksof": [{"id": "1"}]
                    },
                    {
                        "id": "2",
                        "title": "file paperwork",
                        "doneStatus": "false",
                        "description": "",
                        "tasksof": [
                            {
                                "id": "1"
                            }
                        ]
                    }
                ]
            }
        
        cls.dishes_json = {
                    
                        "title": "wash dishes",
                        "doneStatus": False,
                        "description": "",
                        
        }
        cls.dishes_json_response = {
                        "id": "3",
                        "title": "wash dishes",
                        "doneStatus": "false",
                        "description": ""
        }

        cls.update_paperwork_json = {
                "title": "scan paperwork",            
                "doneStatus": True,
                "description" : "all paperwork has been scanned"

        }
        
        cls.update_paperwork_json_response = {
                        "id": "1",
                        "title": "scan paperwork",
                        "doneStatus": "true",
                        "description": "all paperwork has been scanned",
                        "categories": [{"id": "1"}],
                        "tasksof": [{"id": "1"}]
        }

        cls.update_paperwork_json_response_put = {
                        "id": "1",
                        "title": "scan paperwork",
                        "doneStatus": "true",
                        "description": "all paperwork has been scanned"
        }   
            
            
    def setUp(self):
        global APPLICATION_RUNNING
        global APPLICATION_PROCESS
        if not APPLICATION_RUNNING:
            try:
                APPLICATION_PROCESS = subprocess.Popen(
                    ["java", "-jar", os.path.join(WORKING_DIR, "runTodoManagerRestAPI-1.5.5.jar")],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=WORKING_DIR,
                    shell=True
                )
                self.wait_for_server()    
                APPLICATION_RUNNING = True
            except Exception as e:
                APPLICATION_RUNNING = False
                print(f"Error starting the application: {e}")
        
        if not APPLICATION_RUNNING:
            raise RuntimeError("The application could not be started and the unit tests have been terminated.")

        
    def tearDown(self):
        global APPLICATION_RUNNING
        global APPLICATION_PROCESS
        try:
            requests.get(f"{BASE_URL}/shutdown")
        except Exception as e:
            pass

        APPLICATION_PROCESS.terminate()  
        APPLICATION_PROCESS.wait()
        APPLICATION_PROCESS = None
        APPLICATION_RUNNING = False


    # Tests get all todos
    def test_get_todos(self):
        response = requests.get(BASE_URL + "/todos", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json, self.expected_json_all_ids, ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")



    # Tests get todo by id
    def test_get_todo(self):
        id = 1
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["todos"][0], self.expected_json_all_ids["todos"][0], ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")



    # Tests get header for all todos
    def test_get_header(self):
        response = requests.head(BASE_URL + f"/todos", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)


    # Tests get header for todo by id
    def test_get_header_id(self):
        id = 1
        response = requests.head(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)



    # Tests post todo
    def test_post_todo(self):
        id = 3
        response = requests.post(BASE_URL + f"/todos", headers={"Accept": "application/json"}, json=self.dishes_json)
        self.assertEqual(response.status_code, 201)
        
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["todos"][0], self.dishes_json_response, ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")


    # Tests post todo by id
    def test_post_todo_by_id(self):
        id = 1
        response = requests.post(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"}, json=self.update_paperwork_json)
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["todos"][0], self.update_paperwork_json_response, ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")



    # Tests put todo by id
    def test_put_todo_by_id(self):
        id = 1
        response = requests.put(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"}, json=self.update_paperwork_json)
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["todos"][0], self.update_paperwork_json_response_put, ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")

    # Tests delete todo by id
    def test_delete_todo_by_id(self):
        id = 2
        response = requests.delete(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)

        expected_error = {"errorMessages": [f"Could not find an instance with todos/{id}"]}
        actual_json = response.json()  
        self.assertEqual(actual_json, expected_error)


    





    @staticmethod
    def wait_for_server():
            while True:
                response = requests.get(f"{BASE_URL}/todos", timeout=3)
                if response.status_code == 200:
                    return 



if __name__ == '__main__':
    unittest.main()
