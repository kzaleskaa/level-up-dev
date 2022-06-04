from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_task_4_1_all():
    response = client.get("/suppliers")
    expected_response = [
        {"SupplierID": 1, "CompanyName": "Exotic Liquids"},
        {"SupplierID": 2, "CompanyName": "New Orleans Cajun Delights"},
        {"SupplierID": 3, "CompanyName": "Grandma Kelly's Homestead"},
        {"SupplierID": 4, "CompanyName": "Tokyo Traders"},
        {"SupplierID": 5, "CompanyName": "Cooperativa de Quesos 'Las Cabras'"}
    ]

    assert response.status_code == 200
    assert response.json()[:5] == expected_response


def test_task_4_1_id_correct():
    response = client.get("/suppliers/5")
    expected_response = {
        "SupplierID": 5,
        "CompanyName": "Cooperativa de Quesos 'Las Cabras'",
        "ContactName": "Antonio del Valle Saavedra",
        "ContactTitle": "Export Administrator",
        "Address": "Calle del Rosal 4",
        "City": "Oviedo",
        "Region": "Asturias",
        "PostalCode": "33007",
        "Country": "Spain",
        "Phone": "(98) 598 76 54",
        "Fax": None,
        "HomePage": None,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


def test_task_4_1_id_incorrect():
    response = client.get("/suppliers/10000")
    assert response.status_code == 404


def test_task_4_2_id_correct():
    response = client.get("/suppliers/12/products")
    expected_response = [
        {
            "ProductID": 77,
            "ProductName": "Original Frankfurter grüne Soße",
            "Category": {"CategoryID": 2, "CategoryName": "Condiments"},
            "Discontinued": 0,
        },
        {
            "ProductID": 75,
            "ProductName": "Rhönbräu Klosterbier",
            "Category": {"CategoryID": 1, "CategoryName": "Beverages"},
            "Discontinued": 0,
        },
        {
            "ProductID": 64,
            "ProductName": "Wimmers gute Semmelknödel",
            "Category": {"CategoryID": 5, "CategoryName": "Grains/Cereals"},
            "Discontinued": 0,
        },
        {
            "ProductID": 29,
            "ProductName": "Thüringer Rostbratwurst",
            "Category": {"CategoryID": 6, "CategoryName": "Meat/Poultry"},
            "Discontinued": 1,
        },
        {
            "ProductID": 28,
            "ProductName": "Rössle Sauerkraut",
            "Category": {"CategoryID": 7, "CategoryName": "Produce"},
            "Discontinued": 1,
        },
    ]

    assert response.status_code == 200
    assert response.json() == expected_response


def test_task_4_2_id_incorrect():
    response = client.get("/suppliers/10000/products")
    assert response.status_code == 404


def test_task_4_3_create_new_supplier():
    input_data = {
        "CompanyName": "Test Company Name",
        "ContactName": "Test Contact Name",
        "ContactTitle": "Unknown",
        "Address": "Test Address",
        "City": "Test City",
        "PostalCode": "123-123",
        "Country": "Unknown",
        "Phone": "123-123-123",
    }
    response = client.post("/suppliers", json=input_data)
    response_json = response.json()

    assert response.status_code == 200

    assert type(response_json["SupplierID"]) == int

    assert response_json["CompanyName"] == "Test Company Name"
    assert response_json["ContactName"] == "Test Contact Name"

    assert response_json["Fax"] is None
    assert response_json["HomePage"] is None


def test_task_4_3_create_new_supplier_input():
    input_data = {
        "CompanyName": "Test Company Name",
    }
    response = client.post("/suppliers", json=input_data)
    response_json = response.json()

    assert response.status_code == 200

    assert type(response_json["SupplierID"]) == int

    assert response_json["CompanyName"] == "Test Company Name"

    assert response_json["Phone"] is None
    assert response_json["Fax"] is None
    assert response_json["HomePage"] is None


def test_task_4_4_update_supplier_info():
    input_data = {
        "CompanyName": "Test Company Name",
    }
    response = client.put("/suppliers/1", json=input_data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["CompanyName"] == "Test Company Name"
    assert response_json["SupplierID"] == 1


def test_task_4_5_delete_supplier():
    input_data = {
        "CompanyName": "Test Company Name",
        "ContactName": "Test Contact Name",
        "ContactTitle": "Unknown",
        "Address": "Test Address",
        "City": "Test City",
        "PostalCode": "123-123",
        "Country": "Unknown",
        "Phone": "123-123-123",
    }
    response_add = client.post("/suppliers", json=input_data)
    response_json = response_add.json()
    new_supplier_id = response_json["SupplierID"]

    response_delete = client.delete(f"/suppliers/{new_supplier_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/suppliers/{new_supplier_id}")
    assert response_get.status_code == 404


def test_task_4_5_no_exist():
    response_delete = client.delete(f"/suppliers/100000")
    assert response_delete.status_code == 404
