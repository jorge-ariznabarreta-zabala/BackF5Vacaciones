# test_vacations.py

import pytest
from models.model_vacations import Vacations

# If you have a test database, you may use it for testing purposes
TEST_DATABASE = "path/to/your/test_database.sqlite"

# Initialize the database for testing
Vacations.DATABASE = TEST_DATABASE
Vacations.create_table()

# Define test data
TEST_VACATION = {
    "id_user": 1,
    "list_days": "2023-07-26, 2023-07-27",
    "approved": "TRUE"
}

def test_create_vacation():
    response, status_code = Vacations.post_vacation(TEST_VACATION)
    assert status_code == 200
    assert response["message"] == "vacation created successfully"

def test_get_vacation_by_id():
    vacation_id = 1
    vacation = Vacations.get_vacation_by_id(vacation_id)
    assert vacation["id"] == vacation_id
    assert vacation["id_user"] == TEST_VACATION["id_user"]

def test_get_all_vacations():
    vacations = Vacations.get_all_vacations()
    assert len(vacations) >= 1

def test_put_vacation():
    vacation_id = 1
    updated_vacation_data = {
        "id_user": 2,
        "list_days": "2023-07-28, 2023-07-29",
        "approved": "FALSE"
    }
    response = Vacations.put_vacation(updated_vacation_data, vacation_id)
    assert response is None

def test_patch_vacation():
    vacation_id = 1
    updated_vacation_data = {
        "list_days": "2023-07-30, 2023-07-31"
    }
    response = Vacations.patch_vacation(updated_vacation_data, vacation_id)
    assert response is None

def test_delete_vacation():
    vacation_id = 1
    Vacations.delete_vacation(vacation_id)
    vacation = Vacations.get_vacation_by_id(vacation_id)
    assert vacation is None
