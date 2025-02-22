import unittest
import subprocess
import requests
import os
from deepdiff import DeepDiff

# Global Test Data Constants

BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
APP_RUNNING = False
APP_PROCESS = None

EXPECTED_JSON_ALL_IDS = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "categories": [{
                "id": "1",
                "title": "Office",
                "description": ""
            }],
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        }
    ]
}





HOME_CATEGORY = {
    "id": "2",
    "title": "Home",
    "description": ""
}

UPDATED_PAPERWORK_BEDROOM_JSON_RESPONSE = {
    "id": "1",
    "title": "scan paperwork",
    "doneStatus": "false",
    "description": "",
    "categories": [{
        "id": "1",
        "title": "master bedroom",
        "description": ""
    }],
    "tasksof": [{"id": "1"}]
}

UPDATED_ALL_IDS_JSON = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        }
    ]
}



POST_UPDATED_JSON_ALL_IDS = {
  "todos": [
    {
      "id": "1",
      "title": "scan paperwork",
      "doneStatus": "false",
      "description": "",
      "categories": [
        {
          "id": "1"
        }
      ],
      "tasksof": [
        {
          "id": "1"
        }
      ]
    },
    {
      "id": "2",
      "title": "file paperwork",
      "doneStatus": "false",
      "description": "",
      "categories": [
        {
          "id": "2"
        }
      ],
      "tasksof": [
        {
          "id": "1"
        }
      ]
    }
  ]
}


class TodoApiUnitTests(unittest.TestCase):

    def setUp(self):
        global EXPECTED_JSON_ALL_IDS, POST_UPDATED_JSON_ALL_IDS
        global HOME_CATEGORY, UPDATED_PAPERWORK_BEDROOM_JSON_RESPONSE, UPDATED_ALL_IDS_JSON

        self.expected_json_all_ids = EXPECTED_JSON_ALL_IDS

        self.home_category = HOME_CATEGORY
        self.updated_paperwork_bedroom_json_response = UPDATED_PAPERWORK_BEDROOM_JSON_RESPONSE
        self.updated_all_ids_json = UPDATED_ALL_IDS_JSON
        self.post_updated_json_all_ids = POST_UPDATED_JSON_ALL_IDS

        global APP_RUNNING, APP_PROCESS
        if not APP_RUNNING:
            try:
                APP_PROCESS = subprocess.Popen(
                    ["java", "-jar", os.path.join(WORKING_DIRECTORY, "runTodoManagerRestAPI-1.5.5.jar")],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=WORKING_DIRECTORY,
                    shell=True
                )
                self.wait_for_server()    
                APP_RUNNING = True
            except Exception as e:
                APP_RUNNING = False
        
        if not APP_RUNNING:
            raise RuntimeError("The application could not be started and the unit tests have been terminated.")

    def tearDown(self):
        global APP_RUNNING, APP_PROCESS
        try:
            requests.get(f"{BASE_URL}/shutdown")
        except Exception:
            pass

        APP_PROCESS.terminate()  
        APP_PROCESS.wait()
        APP_PROCESS = None
        APP_RUNNING = False

    # Tests getting cateogries for a specific TODO
    def test_get_todo_categories(self):
        todo_id = 1
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["categories"], self.expected_json_all_ids["todos"][0]["categories"], ignore_order=True)
        self.assertEqual(diff, {})

        # Ensures there are no side effects after the request
        self.no_side_effects_for_non_modifying_requests(self)

    # Tests getting cateogries for a specific TODO with a nonexistent ID
    # Note: This test is implemented with the expected output and fails due to a bug
    def test_get_todo_categories_non_existent_id_bug(self):
        todo_id = 99
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 404)

        self.no_side_effects_for_non_modifying_requests(self)

    
    # Note: This test is designed to pass for the bug and verifies the actual behaviour
    def test_get_todo_categories_non_existent_id_success(self):
        todo_id = 99
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})    
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)




    # Tests getting head of cateogries for a specific TODO and cateogry
    def test_head_todo_categories(self):
        todo_id = 1
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)



        
    # Tests head of cateogries for a specific TODO with a nonexistent ID
    # Note: This test is implemented with the expected output and fails due to a bug
    def test_head_todo_categories_non_existent_id_bug(self):
        todo_id = 99
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)


    # Tests head of cateogries for a specific TODO with a nonexistent ID
    # Note: This test is designed to pass and verifies the actual (buggy) behvaiour
    def test_head_todo_categories_non_existent_id_success(self):
        todo_id = 99
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)



    # Tests posting a new todo cateogry relatiionship isntance for a specific TODO with an ID
    def test_post_todo_categories(self):
        todo_id = 2
        response = requests.post(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"}, json=self.home_category) 
        self.assertEqual(response.status_code, 201)
        
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        
        # Ensure that the post request actually makes the specified changes
        diff = DeepDiff(actual_json["categories"][0], self.home_category, ignore_order=True)
        self.assertEqual(diff, {})

        # Ensures there are no side effects after the request
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json, self.post_updated_json_all_ids, ignore_order=True)
        self.assertEqual(diff, {})
       

    # Error Case Test: Tests posting a new todo cateogry relatiionship isntance for a specific TODO with a non existent todo ID
    def test_post_todo_categories_non_existent_id(self):
        todo_id = 99
        response = requests.post(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"}, json=self.home_category) 
        self.assertEqual(response.status_code, 404)
        

        actual_error_message = response.json().get("errorMessages", [""])[0]
        expected_error_message = f"Could not find parent thing for relationship todos/{todo_id}/categories"
        self.assertEqual(actual_error_message, expected_error_message)
        self.no_side_effects_for_non_modifying_requests(self)


        self.no_side_effects_for_non_modifying_requests(self)


    # Tests posting a new todo cateogry relatiionship isntance for a specific TODO with a non existent category ID
    def test_post_todo_categories_category_non_existent_id(self):
        todo_id = 1
        self.home_category["id"] = 99
        response = requests.post(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/json"}, json=self.home_category) 
        self.home_category["id"] = 2
        self.assertEqual(response.status_code, 404)
        
        
        actual_error_message = response.json().get("errorMessages", [""])[0]
        expected_error_message = f"Could not find thing matching value for id"
        self.assertEqual(actual_error_message, expected_error_message)
        self.no_side_effects_for_non_modifying_requests(self)





    # Test: DELETE a todo's category by id
    def test_delete_todo_categories(self):
        todo_id = 1
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        
        # Ensures there are no side effects after the request
        diff = DeepDiff(actual_json, self.updated_all_ids_json, ignore_order=True)
        self.assertEqual(diff, {})


    # Error Case Test: DELETE a todo's category by id
    def test_delete_todo_categories_non__existent_id(self):
        todo_id = 99
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)

        self.no_side_effects_for_non_modifying_requests(self)
        
    
    
    # Error Case Test: DELETE a specific todo's category by id two times
    def test_delete_todo_categories_double(self):
        todo_id = 1
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)

        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)




    # Assert that there are no unexpected side effects for non-modifying requests
    @staticmethod
    def no_side_effects_for_non_modifying_requests(self):

        # Verifies that first todo has the expected categories
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/1/categories", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["categories"], self.expected_json_all_ids["todos"][0]["categories"], ignore_order=True)
        self.assertEqual(diff, {})

        # Verifies that second todo has the expected categories  
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/2/categories", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["categories"], [], ignore_order=True)
        self.assertEqual(diff, {})


    
    
    @staticmethod
    def wait_for_server():
        while True:
            response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", timeout=3)
            if response.status_code == 200:
                return


if __name__ == '__main__':
    unittest.main()
