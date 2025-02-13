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
                cls.wait_for_server()    
                APPLICATION_RUNNING = True
            except Exception as e:
                APPLICATION_RUNNING = False
                print(f"Error starting the application: {e}")
        
        if not APPLICATION_RUNNING:
            raise RuntimeError("The application could not be started and the unit tests have been terminated.")
        
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


    @classmethod
    def tearDownClass(cls):
        global APPLICATION_PROCESS
        try:
            requests.get(f"{BASE_URL}/shutdown")
        except Exception as e:
            pass

        APPLICATION_PROCESS.terminate()  
        APPLICATION_PROCESS.wait()
        APPLICATION_PROCESS = None



    def test_get_todos(self):
        response = requests.get(BASE_URL + "/todos", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json, self.expected_json_all_ids, ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")



    def test_get_todo(self):
        id = 1
        response = requests.get(BASE_URL + f"/todos/{id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["todos"][0], self.expected_json_all_ids["todos"][0], ignore_order=True)
        self.assertEqual(diff, {}, f"Differences found: {diff}")


    




    @staticmethod
    def wait_for_server():
        while True:
            response = requests.get(f"{BASE_URL}/todos", timeout=3)
            if response.status_code == 200:
                return 
            time.sleep(2)  



if __name__ == '__main__':
    unittest.main()
