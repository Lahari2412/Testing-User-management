# UserManagement_RestAPI

## Testing
---------------------------------

## What is testing?

- Software testing is an important process in the software development lifecycle . It involves verifying and validating that a software application is free of bugs, meets the technical requirements set by its design and development , and satisfies user requirements efficiently and effectively.

- Software Testing is a method to assess the functionality of the software program. The process checks whether the actual software matches the expected requirements and ensures the software is bug-free. The purpose of software testing is to identify the errors, faults, or missing requirements in contrast to actual requirements. It mainly aims at measuring the specification, functionality, and performance of a software program or application.


## Why do we need testing
--------------------------------------------

Testing is a crucial part of the software development process for several reasons:

1. **Catch Bugs Early**: Testing helps identify errors and bugs in the code before they reach production. The earlier you catch a bug, the less costly it is to fix.

2. **Ensure Code Quality**: Automated tests ensure that your code behaves as expected, improving overall quality and reliability. Well-tested code leads to fewer issues when the software is deployed.

3. **Prevent Regressions**: As the application evolves, changes in one area can inadvertently break functionality in another. Testing ensures that new features don’t negatively affect existing code (regression).

4. **Validate Requirements**: Tests help confirm that the application behaves according to the specified requirements and meets the users' needs. This is especially important when dealing with complex systems.

5. **Save Time and Money**: While writing tests requires an upfront investment of time, it saves effort in the long run by reducing debugging time, minimizing post-release issues, and lowering maintenance costs.

6. **Enable Confident Refactoring**: Tests give developers confidence to refactor or improve the codebase without the fear of breaking existing functionality.

7. **Facilitate Collaboration**: Testing improves team collaboration by ensuring that changes made by one developer don’t disrupt the work of others. It helps maintain a stable codebase.

8. **Support Continuous Integration/Deployment (CI/CD)**: Automated testing is an integral part of CI/CD pipelines, enabling continuous development and faster release cycles.

9. **Improve Documentation**: Tests act as a form of live documentation, showing how different parts of the system are expected to work. This can be useful for onboarding new developers.


## Testing in Fastapi
-------------------------------

In FastAPI, testing involves writing code to verify that your API endpoints, business logic, and data handling work as expected. This ensures that your application behaves correctly under various conditions and that any changes you make don't introduce bugs.

To effectively test a FastAPI application, you need a few key tools, libraries, and practices. Here's what's required:

1. **Python and FastAPI Installed**

   - **Python**: You need Python installed on your machine, typically version 3.7 or later.

   - **FastAPI**: Your FastAPI application should be set up and running. You can install it using pip:

     ```bash
     pip install fastapi
     ```

2. **Testing Framework: `pytest`**

   - **`pytest`**: A popular testing framework in Python, `pytest` makes it easy to write and run tests.

     - Install it using pip:

       ```bash
       pip install pytest
       ```

   - **`pytest-asyncio`**: If your FastAPI application uses asynchronous code, this plugin is necessary to test async functions.

     - Install it using pip:

       ```bash
       pip install pytest-asyncio
       ```

3. **HTTP Client for Testing: `TestClient` or `httpx`**

   - **`TestClient`**: FastAPI provides a `TestClient` class, built on top of `requests`, for testing API endpoints.

     - You can import it directly from `fastapi.testclient`:

       ```python
       from fastapi.testclient import TestClient
       ```

   - **`httpx`**: For testing asynchronous endpoints, you can use `httpx.AsyncClient`.

     - Install `httpx` with:

       ```bash
       pip install httpx
       ```
4. **Database Testing Tools**

   - If your application interacts with a database, you need tools to manage test databases:

     - **Test Database**: Set up a separate database or use an in-memory database (e.g., SQLite in-memory) for testing.

     - **Database Fixtures**: Use `pytest` fixtures to manage the setup and teardown of the test database. For MongoDB, you might use `motor` or similar libraries to handle database interactions.

5. **Mocking Libraries (Optional)**

   - **`unittest.mock`**: Part of Python's standard library, used to mock objects and functions during tests.

     ```python
     from unittest.mock import patch
     ```

   - **`pytest-mock`**: An optional plugin that provides a `mocker` fixture to simplify mocking in pytest.
   
     - Install it with:

     ```bash
     pip install pytest-mock
     ```

6. **Environment for Running Tests**

   - **Test Configuration**: Ensure your application can run in a test environment, with settings like database URLs and API keys appropriately configured for testing.

   - **`dotenv` (Optional)**: Use `python-dotenv` to manage environment variables in different environments (e.g., testing vs. production).

     - Install it with:
     
     ```bash
     pip install python-dotenv
     ```

## Example Testing Workflow

1. **Create Test Files**: Place your test files in a dedicated directory (commonly named tests) and follow the naming convention test_*.py.

2. **Use Standard Naming**: Write test functions whose names start with test_ (this is the standard pytest convention).

3. **Write Unit Tests**: Create test functions that verify the behavior of individual units of your code (e.g., functions, methods).

4. **Run Tests**: Use `pytest` to run the tests.

   ```bash
   pytest
   ```


## Example

---

- **Step 1: Create a Simple FastAPI Application**

  Save this in a file named `main.py`:

  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/")
  def read_root():
      return {"message": "Hello, World!"}

  @app.get("/items/{item_id}")
  def read_item(item_id: int, q: str = None):
      return {"item_id": item_id, "q": q}
  ```

  This application has two endpoints:
  
  - `GET /`: Returns a simple message.

  - `GET /items/{item_id}`: Returns an item based on the `item_id` passed in the URL.

---

- **Step 2: Write Tests for the Application**

  Next, create a test file named `test_main.py`. This file will contain tests for the FastAPI application.

  ```python
  from fastapi.testclient import TestClient
  from main import app

  client = TestClient(app)

  def test_read_root():
      response = client.get("/")
      assert response.status_code == 200
      assert response.json() == {"message": "Hello, World!"}

  def test_read_item():
      response = client.get("/items/42?q=somequery")
      assert response.status_code == 200
      assert response.json() == {"item_id": 42, "q": "somequery"}

  def test_read_item_no_query():
      response = client.get("/items/42")
      assert response.status_code == 200
      assert response.json() == {"item_id": 42, "q": None}
  ```

---

- **Step 3: Run the Tests**

  To run the tests, open your terminal or command prompt and run:

  ```bash
  pytest
  ```

  You should see an output indicating that all tests have passed:

  ```plaintext
  ============================= test session starts ==============================
  ...
  collected 3 items

  test_main.py ...                                                            [100%]

  ============================== 3 passed in 0.12s ===============================
  ```


##  Test cases explanation
---------------------------------------


### **Testing user routes**:`test_routes_user.py`


- **Fixture**: `setup_db`

  - **Description**: Sets up and tears down the test database. It drops the `user` collection before the tests run and drops it again after the tests complete to ensure a clean state.

```python
@pytest.fixture(scope="module")
def setup_db():
    # Ensure the user collection is empty before tests
    conn.local.user.drop()
    conn.local.counters.drop()  # Ensure counters collection is also empty for sequence values
    yield
    conn.local.user.drop()
    conn.local.counters.drop()
```

#### Test Case 1: Create a New User

- **Test Case**: `test_create_user`

- **Test Description**: Verify that a new user can be created successfully using the `/api/v1/user/` endpoint.

- **Preconditions**: The application server is running and the database is accessible and empty.

- **Test Steps**:

  1. Send a POST request to `/api/v1/user/` with the payload:

  ```json
  {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "mobile_number": 1234567890,
    "location": "Test Location",
    "password": "Password123!"
  }
  ```

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `201 Created`.

  - The response body should include the user details, with the email matching the input.

- **Actual Result**: 

  - The response status code is `201 Created`.

  - The response body contains user details with the email `"johndoe@example.com"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_user(setup_db):
    response = client.post(
        "/api/v1/user/",
        json={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "mobile_number": 1234567890,
            "location": "Test Location",
            "password": "Password123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "johndoe@example.com"
```

---

#### Test Case 2: Retrieve All Users

- **Test Case**: `test_find_all_users`

- **Test Description**: Verify that the list of users can be retrieved successfully using the `/api/v1/user/` endpoint.

- **Preconditions**: The application server is running, and at least one user is created in the database.

  1. Send a GET request to `/api/v1/user/`.

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `200 OK`.

  - The response body should be a list of users.

- **Actual Result**: 

  - The response status code is `200 OK`.

  - The response body contains a list of users.

- **Pass/Fail Criteria**: Pass.

**Test Case Cod:**

```python
def test_find_all_users(setup_db):
    # Create a user first
    client.post(
        "/api/v1/user/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location",
            "password": "Password123!"
        }
    )
    
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Expect a list of users
```

---

#### Test Case 3: Retrieve a Single User

- **Test Case**: `test_get_user`

- **Test Description**: Verify that a single user can be retrieved successfully using the `/api/v1/user/{id}` endpoint.

- **Preconditions**: The application server is running, and the user has been created.

- **Test Steps**:

  1. Send a GET request to `/api/v1/user/{id}` with the user ID.

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `200 OK`.

  - The response body should include the user details.

- **Actual Result**: 

  - The response status code is `200 OK`.

  - The response body contains the user details, with the email `"alicesmith@example.com"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_get_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Alice Smith",
            "email": "alicesmith@example.com",
            "mobile_number": 1122334455,
            "location": "Some Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test getting the user
    response = client.get(f"/api/v1/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alicesmith@example.com"
```

---

#### Test Case 4: Update a User

- **Test Case**: `test_update_user`

- **Test Description**: Verify that a user can be updated successfully using the `/api/v1/user/{id}` endpoint.

- **Preconditions**: The application server is running, and the user has been created.

- **Test Steps**:

  1. Send a PUT request to `/api/v1/user/{id}` with the payload:

  ```json
  {
    "name": "Bob Updated"
  }
  ```

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `200 OK`.

  - The response body should include the updated user details.

- **Actual Result**: 

  - The response status code is `200 OK`.

  - The response body contains the updated name `"Bob Updated"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_update_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Bob Brown",
            "email": "bobbrown@example.com",
            "mobile_number": 2233445566,
            "location": "New Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test updating the user
    update_response = client.put(
        f"/api/v1/user/{user_id}",
        json={
            "name": "Bob Updated",
            "password": "NewPassword123!"
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Bob Updated"
```

---

#### Test Case 5: Delete a User

- **Test Case**: `test_delete_user`

- **Test Description**: Verify that a user can be deleted successfully using the `/api/v1/user/{id}` endpoint.

- **Preconditions**: The application server is running, and the user has been created.

- **Test Steps**:

  1. Send a DELETE request to `/api/v1/user/{id}`.

  2. Capture the response.

  3. Verify that the user is deleted by sending a GET request to `/api/v1/user/{id}`.

- **Expected Result**:

  - The DELETE response status code should be `200 OK`.

  - The GET response status code should be `404 Not Found`.

- **Actual Result**: 

  - The DELETE response status code is `200 OK`, and the user is successfully deleted.

  - The GET request returns `404 Not Found`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_delete_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Charlie Black",
            "email": "charlieblack@example.com",
            "mobile_number": 6677889900,
            "location": "Delete Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test deleting the user
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"User with id {user_id} deleted successfully"}

    # Verify user is deleted
    get_response = client.get(f"/api/v1/user/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == f"User with id {user_id} not found"
```

---

#### Test Case 6: Create User with Existing Email

- **Test Case**: `test_create_user_with_existing_email`

- **Test Description**: Verify that trying to create a user with an existing email results in an error.

- **Preconditions**: The application server is running, and the user with the email already exists in the database.

- **Test Steps**:

  1. Send a POST request to `/api/v1/user/` with the payload using an email that already exists.

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `422 Unprocessable Entity`.

  - The error message should indicate that the user with the given email already exists.

- **Actual Result**: 

  - The response status code is `422 Unprocessable Entity`.

  - The error message indicates that the user with email `"alicesmith@example.com"` already exists.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_create_user_with_existing_email(setup_db):
    # Create a user first
    client.post(
        "/api/v1/user/",
        json={
            "name": "Alice Smith",
            "email": "alicesmith@example.com",
            "mobile_number": 1234567890,
            "location": "Duplicate Test Location",
            "password": "Password123!"
        }
    )

    # Try creating another user with the same email
    response = client.post(
        "/api/v1/user/",
        json={
            "name": "Duplicate User",
            "email": "alicesmith@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location",
            "password": "Password123!"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "User with this email already exists"
``` 

---

#### Test Case 7: Create User with Invalid Data

- **Test Case**: `test_create_user_invalid_data`

- **Test Description**: Verify that creating a user with missing required fields results in a validation error.

- **Preconditions**: The application server is running, and the required fields for the user (email and password) are omitted in the request payload.

- **Test Steps**:

  1. Send a POST request to `/api/v1/user/` with an incomplete payload, missing required fields (e.g., email and password).

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `422 Unprocessable Entity`.

  - The error message should indicate that required fields are missing.

- **Actual Result**: 

  - The response status code is `422 Unprocessable Entity`.

  - The error message points to missing required fields (email, password, etc.).

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_create_user_invalid_data(setup_db):
    # Test missing required fields (email, password, mobile_number, and location)
    response = client.post(
        "/api/v1/user/",
        json={
            "name": "Invalid User",  # Name is provided
            "email": None,  # Missing email
            "password": None,  # Missing password
            "mobile_number": None,  # Missing mobile number
            "location": None  # Missing location
        }
    )
    assert response.status_code == 422  # Validation error
```

---

#### Test Case 8: Update User with No Changes

- **Test Case**: `test_update_user_no_changes`

- **Test Description**: Verify that trying to update a user without making any changes results in an appropriate error message.

- **Preconditions**: The application server is running, and the user has been created.

- **Test Steps**:

  1. Create a user using a POST request.

  2. Attempt to update the same user with identical data (i.e., no actual changes).

  3. Capture the response.

- **Expected Result**: 

  - The response status code should be `400 Bad Request`.

  - The error message should indicate that no changes were made during the update.

- **Actual Result**: 

  - The response status code is `400 Bad Request`.

  - The error message says "Failed to update user."

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_update_user_no_changes(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Bob Brown",
            "email": "bobb@example.com",
            "mobile_number": 2233445566,
            "location": "New Location",
            "password": "Password123!"
        }
    )
    
    assert create_response.status_code == 201, f"User creation failed: {create_response.json()}"
    
    create_data = create_response.json()
    assert "id" in create_data, f"Expected 'id' in response, got {create_data}"
    
    user_id = create_data["id"]

    # Attempt to update the user with the same data
    update_response = client.put(
        f"/api/v1/user/{user_id}",
        json={
            "name": "Bob Brown",  # No actual changes
        }
    )
    assert update_response.status_code == 400, f"Unexpected response: {update_response.json()}"
    assert update_response.json()["detail"] == "Failed to update user"
```

---

#### Test Case 9: Retrieve Non-Existent User

- **Test Case**: `test_get_user_not_found`

- **Test Description**: Verify that trying to retrieve a non-existent user returns a 404 error.

- **Preconditions**: The application server is running, and the user does not exist in the database.

- **Test Steps**:

  1. Send a GET request to `/api/v1/user/9999` using an invalid or non-existent user ID.

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `404 Not Found`.

  - The error message should indicate that the user with the given ID was not found.

- **Actual Result**: 

  - The response status code is `404 Not Found`.

  - The error message states that the user with ID `9999` was not found.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_get_user_not_found(setup_db):
    # Attempt to get a non-existent user
    response = client.get("/api/v1/user/9999")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 9999 not found"}
```

---

#### Test Case 10: Delete Non-Existent User

- **Test Case**: `test_delete_user_not_found`

- **Test Description**: Verify that trying to delete a non-existent user returns a 404 error.

- **Preconditions**: The application server is running, and the user does not exist in the database.

- **Test Steps**:

  1. Send a DELETE request to `/api/v1/user/9999` using an invalid or non-existent user ID.

  2. Capture the response.

- **Expected Result**: 

  - The response status code should be `404 Not Found`.

  - The error message should indicate that the user with the given ID was not found.

- **Actual Result**: 

  - The response status code is `404 Not Found`.

  - The error message states that the user with ID `9999` was not found.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_delete_user_not_found(setup_db):
    # Attempt to delete a non-existent user
    response = client.delete("/api/v1/user/9999")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 9999 not found"}
```


------------------------------------

### **Testing login_router routes**:`test_login_router.py`


#### Test Case 1: Successful Login

- **Test Case**: `test_login_successful`

- **Test Description**: Verify that a user can log in successfully with valid credentials using the `/api/v1/login/` endpoint.

- **Preconditions**: The application server is running, and a user with the specified email and password exists in the database.

- **Test Steps**:

  1. Create a user with the email `"testuser@example.com"` and password `"ValidPassword123!"`.

  2. Send a POST request to `/api/v1/login/` with the email and password.

  3. Capture the response.

- **Expected Result**:

  - The response status code should be `200 OK`.

  - The response body should include a success message .
- **Actual Result**:

  - The response status code is `200 OK`.

  - The response body contains the message `"Login Successful"` .

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_login_successful(setup_db):
    create_user("testuser@example.com", "ValidPassword123!")
    
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "testuser@example.com",
            "password": "ValidPassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login Successful"
```

---

#### Test Case 2: Login with Invalid Password

- **Test Case**: `test_login_invalid_password`

- **Test Description**: Verify that logging in with an incorrect password results in an error.

- **Preconditions**: The application server is running, and a user with the specified email and a valid password exists in the database.

- **Test Steps**:

  1. Create a user with the email `"testuser@example.com"` and password `"ValidPassword123!"`.

  2. Send a POST request to `/api/v1/login/` with the correct email but an incorrect password `"InValidPassword13!2"`.

  3. Capture the response.

- **Expected Result**:

  - The response status code should be `401 Unauthorized`.

  - The error message should indicate invalid credentials.

- **Actual Result**:

  - The response status code is `401 Unauthorized`.

  - The response body contains the error message `"Invalid email or password"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_login_invalid_password(setup_db):
    create_user("testuser@example.com", "ValidPassword123!")
    
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "testuser@example.com",
            "password": "InValidPassword13!2"
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}
```

---

#### Test Case 3: Login with Non-Existent User

- **Test Case**: `test_login_non_existent_user`

- **Test Description**: Verify that trying to log in with an email that does not exist in the database results in an error.

- **Preconditions**: The application server is running, and no user with the specified email exists in the database.

- **Test Steps**:

  1. Send a POST request to `/api/v1/login/` with an email `"nonexistentuser@example.com"` and a password `"SomePassword123!"`.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `404 Not Found`.

  - The error message should indicate that the user was not found.

- **Actual Result**:

  - The response status code is `404 Not Found`.

  - The response body contains the error message `"User not found"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_login_non_existent_user(setup_db):
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "nonexistentuser@example.com",
            "password": "SomePassword123!"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
```

---

**Test Utilities**

- **Fixture**: `setup_db`

  - **Description**: Sets up and tears down the test database. It drops the `user` collection before the tests run and drops it again after the tests complete to ensure a clean state.


### **Testing Password Reset Routes**: `test_routes_password_reset.py`

#### Test Case 1: Successful Password Reset

- **Test Case**: `test_reset_password_success`

- **Test Description**: Verify that a user can successfully reset their password using the `/api/v1/password_reset/{email}` endpoint.

- **Preconditions**: The application server is running, and a user with the email `"test@example.com"` exists in the database with an old hashed password.

- **Test Steps**:

  1. Send a PUT request to `/api/v1/password_reset/test@example.com` with a JSON payload containing the new password `"NewPassword123!"`.

  2. Capture the response.

  3. Verify that the password has been updated in the database.

- **Expected Result**:

  - The response status code should be `200 OK`.

  - The response body should contain a success message: `"Password reset successful"`.

- **Actual Result**:

  - The response status code is `200 OK`.

  - The response body contains the message `"Password reset successful"`.


- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_reset_password_success(setup_db):
    response = client.put(
        "/api/v1/password_reset/test@example.com",
        json={"new_password": "NewPassword123!"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset successful"}

    # Verify password has been updated in the database
    user_collection = conn.local.user
    updated_user = user_collection.find_one({"email": "test@example.com"})
    assert updated_user is not None
    assert updated_user["password"] != "OldHashedPassword123!"  # Password should be changed
```

---

#### Test Case 2: Password Reset for Non-Existent User

- **Test Case**: `test_reset_password_user_not_found`

- **Test Description**: Verify that trying to reset the password for an email that does not exist in the database returns an appropriate error.

- **Preconditions**: The application server is running, and no user with the email `"nonexistent@example.com"` exists in the database.

- **Test Steps**:

  1. Send a PUT request to `/api/v1/password_reset/nonexistent@example.com` with a JSON payload containing the new password `"NewPassword123!"`.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `404 Not Found`.

  - The error message should indicate that the user with the given email was not found.

- **Actual Result**:

  - The response status code is `404 Not Found`.

  - The response body contains the error message `"User with the given email not found"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_reset_password_user_not_found(setup_db):
    response = client.put(
        "/api/v1/password_reset/nonexistent@example.com",
        json={"new_password": "NewPassword123!"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User with the given email not found"}
```

---

#### Test Case 3: Password Reset with Invalid Password

- **Test Case**: `test_reset_password_invalid_password`

- **Test Description**: Verify that attempting to reset the password with a new password that does not meet validation criteria returns an appropriate error.

- **Preconditions**: The application server is running, and a user with the email `"test@example.com"` exists in the database.

- **Test Steps**:

  1. Send a PUT request to `/api/v1/password_reset/test@example.com` with a JSON payload containing a new password that is too short, `"short"`.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `422 Unprocessable Entity`.

  - The error message should indicate that the password must meet the required length or other criteria.

- **Actual Result**:

  - The response status code is `422 Unprocessable Entity`.

  - The response body contains the error message `"Password must be at least 8 characters long"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_reset_password_invalid_password(setup_db):
    response = client.put(
        "/api/v1/password_reset/test@example.com",
        json={"new_password": "short"}
    )
    assert response.status_code == 422
    assert response.json() == {"message": "Password must be at least 8 characters long"}
```

---

**Test Utilities**

- **Fixture**: `setup_db`

  - **Description**: Prepares the test database by clearing the `user` collection and inserting a test user before each test. It also clears the collection after each test to ensure a clean state.

------------------------------------------

### **Testing Admin Creation Routes**: `test_routes_admin.py`

#### Test Case 1: Successful Admin User Creation

- **Test Case**: `test_create_admin_user`

- **Test Description**: Verify that an admin user can be created successfully using the `/api/v1/admin/` endpoint.

- **Preconditions**: The application server is running, and the `user` and `counters` collections are empty.

- **Test Steps**:

  1. Send a POST request to `/api/v1/admin/` with a JSON payload containing the admin user details, including name, email, mobile number, and location.

  2. Capture the response.

  3. Verify that the response status code is `201 Created`.

  4. Check that the response body contains the correct email.

  5. Verify that the user is correctly inserted into the database with the expected details and a hashed password.

- **Expected Result**:

  - The response status code should be `201 Created`.

  - The response body should include the email `"john.doe@example.com"`.

  - The user should be present in the database with the provided name and a hashed password.

- **Actual Result**:

  - The response status code is `201 Created`.

  - The response body contains the email `"john.doe@example.com"`.

  - The user is correctly inserted into the database with the expected details and a hashed password.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_admin_user(setup_db):
    admin_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "mobile_number": 1234567890,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == "john.doe@example.com"

```

---

#### Test Case 2: Create Admin User with Duplicate Email

- **Test Case**: `test_create_admin_user_duplicate_email`

- **Test Description**: Verify that attempting to create an admin user with an email that already exists in the database results in an error.

- **Preconditions**: The application server is running, and an admin user with the email `"john.doe@example.com"` already exists in the database.

- **Test Steps**:

  1. Send a POST request to `/api/v1/admin/` with a JSON payload containing an admin user with the email `"john.doe@example.com"`.

  2. Capture the response.

  3. Send another POST request to `/api/v1/admin/` with the same email to test for duplication.

  4. Capture the response of the second request.

- **Expected Result**:

  - The response status code for the second request should be `422 Unprocessable Entity`.

  - The error message should indicate that the user with the given email already exists.

- **Actual Result**:

  - The response status code is `422 Unprocessable Entity`.

  - The response body contains the error message `"User with this email already exists"`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_admin_user_duplicate_email(setup_db):
    admin_data = {
        "name": "Jane Doe",
        "email": "john.doe@example.com",
        "mobile_number": 1234567891,
        "location": "Test Location"
    }
    client.post("/api/v1/admin/", json=admin_data)

    # Attempt to create a user with the same email
    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422
    error_message = response.json().get("detail") or response.json().get("message")
    
    # Adjust assertion to handle the prefix
    expected_message = "User with this email already exists"
    assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"
```

---

#### Test Case 3: Create Admin User with Invalid Email

- **Test Case**: `test_create_admin_user_invalid_email`

- **Test Description**: Verify that attempting to create an admin user with an invalid email format results in an error.

- **Preconditions**: The application server is running, and the `user` and `counters` collections are empty.

- **Test Steps**:

  1. Send a POST request to `/api/v1/admin/` with a JSON payload containing an invalid email format `"invalid-email"`.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `422 Unprocessable Entity`.

  - The response body should include validation error details indicating that the email format is invalid.

- **Actual Result**:

  - The response status code is `422 Unprocessable Entity`.

  - The response body contains validation error details indicating the email format is invalid.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_admin_user_invalid_email(setup_db):
    invalid_admin_data = {
        "name": "Jake Doe",
        "email": "invalid-email",
        "mobile_number": 1234567892,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=invalid_admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details
```

---

#### Test Case 4: Create Admin User with Missing Required Field

- **Test Case**: `test_create_admin_user_missing_field`

- **Test Description**: Verify that attempting to create an admin user with missing required fields results in an error.

- **Preconditions**: The application server is running, and the `user` and `counters` collections are empty.

- **Test Steps**:

  1. Send a POST request to `/api/v1/admin/` with a JSON payload that is missing the required `mobile_number` field.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `422 Unprocessable Entity`.

  - The response body should include validation error details indicating that the `mobile_number` field is missing.

- **Actual Result**:

  - The response status code is `422 Unprocessable Entity`.

  - The response body contains validation error details indicating that the `mobile_number` field is missing.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_create_admin_user_missing_field(setup_db):
    admin_data = {
        "name": "Emily Doe",
        "email": "emily.doe@example.com",
        "location": "Test Location"  # Missing mobile_number
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details
```

---

#### Test Case 5: Create Admin User with Invalid Mobile Number

- **Test Case**: `test_create_admin_user_invalid_mobile_number`

- **Test Description**: Verify that attempting to create an admin user with an invalid mobile number format results in an error.

- **Preconditions**: The application server is running, and the `user` and `counters` collections are empty.

- **Test Steps**:

  1. Send a POST request to `/api/v1/admin/` with a JSON payload containing an invalid mobile number format.

  2. Capture the response.

- **Expected Result**:

  - The response status code should be `422 Unprocessable Entity`.

  - The response body should include validation error details indicating that the mobile number format is invalid.

- **Actual Result**:

  - The response status code is `422 Unprocessable Entity`.

  - The response body contains validation error details indicating the invalid mobile number format.

- **Pass/Fail Criteria**: Pass.

**Test Case Code**:

```python
def test_create_admin_user_invalid_mobile_number(setup_db):
    admin_data = {
        "name": "Lucas Doe",
        "email": "lucas.doe@example.com",
        "mobile_number": "7896056",  # Invalid format
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details
```

---

**Test Utilities**

- **Fixture**: `setup_db`

  - **Description**: Prepares the test database by clearing the `user` and `counters` collections before each test. It also clears the collections after each test to ensure a clean state.

------------------------------------------------------

### **Testing Panel Member Routes**: `test_routes_member.py`

#### Test Case 1: Create Member

- **Test Case**: `test_create_member`

- **Test Description**: Verify that a member can be successfully created using the `/api/v1/member/` endpoint.

- **Preconditions**: The application server is running, and the members collection is empty.

- **Test Steps**:
  
  1. Send a POST request to `/api/v1/member/` with valid member data including name, email, mobile number, location, and password.
  
  2. Capture the response.

- **Expected Result**:
  
  - The response status code should be 201 Created.
  
  - The response body should contain the newly created member's `id` and `email`.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_member(setup_db):
    response = client.post(
        "/api/v1/member/",
        json={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "mobile_number": 1234567890,
            "location": "Test Location",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "johndoe@example.com"
```

---

#### Test Case 2: Find All Members

- **Test Case**: `test_find_all_members`

- **Test Description**: Verify that all members can be retrieved using the `/api/v1/member/` endpoint.

- **Preconditions**: The application server is running, and at least one member exists in the database.

- **Test Steps**:
  
  1. Create a member.
  
  2. Send a GET request to `/api/v1/member/` to retrieve all members.
  
  3. Capture the response.

- **Expected Result**:
  
  - The response status code should be 200 OK.
  
  - The response body should contain a list of members.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_find_all_members(setup_db):
    client.post(
        "/api/v1/member/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location"
        }
    )
    
    response = client.get("/api/v1/member/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

---

#### Test Case 3: Get Member by ID

- **Test Case**: `test_get_member`

- **Test Description**: Verify that a member can be retrieved by their ID using the `/api/v1/member/{id}` endpoint.

- **Preconditions**: The application server is running, and a member with the given ID exists.

- **Test Steps**:
  
  1. Create a member.
  
  2. Send a GET request to `/api/v1/member/{id}` with the newly created member's ID.
  
  3. Capture the response.

- **Expected Result**:
  
  - The response status code should be 200 OK.
  
  - The response body should contain the member's information.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_get_member(setup_db):
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Alice Smith",
            "email": "alicesmith@example.com",
            "mobile_number": 1122334455,
            "location": "Some Location"
        }
    )
    member_id = create_response.json()["id"]

    response = client.get(f"/api/v1/member/{member_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alicesmith@example.com"
```

---

#### Test Case 4: Update Member

- **Test Case**: `test_update_member`

- **Test Description**: Verify that a member's information can be updated using the `/api/v1/member/{id}` endpoint.

- **Preconditions**: The application server is running, and a member with the given ID exists.

- **Test Steps**:
  
  1. Create a member.
  
  2. Send a PUT request to `/api/v1/member/{id}` with updated member data.
  
  3. Capture the response.

- **Expected Result**:
  
  - The response status code should be 200 OK.
  
  - The response body should reflect the updated member's data.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_update_member(setup_db):
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Bob Brown",
            "email": "bobbrown@example.com",
            "mobile_number": 2233445566,
            "location": "New Location"
        }
    )
    member_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/member/{member_id}",
        json={
            "name": "Bob Updated",
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Bob Updated"
```

---

#### Test Case 5: Delete Member

- **Test Case**: `test_delete_member`

- **Test Description**: Verify that a member can be deleted using the `/api/v1/member/{id}` endpoint.

- **Preconditions**: The application server is running, and a member with the given ID exists.

- **Test Steps**:
  
  1. Create a member.
  
  2. Send a DELETE request to `/api/v1/member/{id}` with the member's ID.
  
  3. Capture the response.

- **Expected Result**:
  
  - The response status code should be 200 OK.
  
  - The response body should contain a success message indicating the member was deleted.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_delete_member(setup_db):
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Charlie Black",
            "email": "charlieblack@example.com",
            "mobile_number": 6677889900,
            "location": "Delete Location"
        }
    )
    member_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/member/{member_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Panel Member with id {member_id} deleted successfully"}

    get_response = client.get(f"/api/v1/member/{member_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == f"Panel Member with id {member_id} not found"
```

---

**Test Utilities**

- **Fixture**: `setup_db`

  - **Description**: This fixture ensures that the test database starts with a clean state. It drops the `members` and `counters` collections before and after the tests.


### **Testing main.py**: `test_main.py`

#### Test Case 1: Find Admin User

- **Test Case**: `test_find_admin`

- **Test Description**: Verify that the `/api/v1/user/` endpoint returns a list of users and the list includes the admin user created during the test setup.

- **Preconditions**: The application server is running, and a user with the email `"admin@gmail.com"` exists in the database.

- **Test Steps**:

  1. Create an admin user with the email `"admin@gmail.com"` and password `"Admin@12345"`.

  2. Send a GET request to `/api/v1/user/` to retrieve the list of users.

  3. Capture the response.

- **Expected Result**:

  - The response status code should be `200 OK`.

  - The response body should be a list of users.

  - The list should contain the created admin user.

- **Actual Result**:

  - The response status code is `200 OK`.

  - The response body is a list of users, which includes the admin user.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_find_admin(setup_db):
    # Create an admin user first
    client.post(
        "/api/v1/user/",
        json={
            "name": "Admin",
            "email": "admin@gmail.com",
            "mobile_number": 9876543210,
            "location": "Another Location",
            "password": "Admin@12345"
        }
    )
    
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Expect a list of users
```

---

#### Test Case 2: Create User

- **Test Case**: `test_create_user`

- **Test Description**: Verify that a user can be created successfully using the `/api/v1/user` endpoint.

- **Preconditions**: The application server is running.

- **Test Steps**:

  1. Send a POST request to `/api/v1/user` with user details including name, email, mobile number, location, password, role, and optional fields.

  2. Capture the response.

  3. Check that the user was successfully created by querying the database.

- **Expected Result**:

  - The response status code should be `201 Created`.

  - The user should be present in the database with the given details.

- **Actual Result**:

  - The response status code is `201 Created`.

  - The user is present in the database with the specified details.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_create_user():
    user_data = {
        "name": "Admin",
        "email": "admin@gmail.com",
        "mobile_number": 9876543210,
        "location": "Test City",
        "password": "Admin@12345",
        "role": "user",
        "whatsapp_api_token": None,
        "whatsapp_cloud_number_id": None
    }
    response = client.post("/api/v1/user", json=user_data)
    assert response.status_code == 201
    created_user = conn.local.user.find_one({"email": "admin@gmail.com"})
    assert created_user is not None
    assert created_user["name"] == "Admin"
```

---


#### Test Case 3: Password Hashing

- **Test Case**: `test_password_hashing`

- **Test Description**: Verify that the password hashing function correctly hashes passwords and the hashed password cannot be easily compared with the plain text password.

- **Preconditions**: The application server is running, and the `get_password_hash` function is available.

- **Test Steps**:

  1. Hash a raw password using the `get_password_hash` function.

  2. Verify that the hashed password does not match the plain text password.

  3. Verify that the hashed password can be used to validate the raw password.

- **Expected Result**:

  - The hashed password should not be the same as the raw password.

  - The `bcrypt.checkpw` function should confirm that the hashed password matches the raw password.

- **Actual Result**:

  - The hashed password does not match the raw password.

  - The `bcrypt.checkpw` function confirms the match.

- **Pass/Fail Criteria**: Pass.

**Test Case Code:**

```python
def test_password_hashing():
    raw_password = "Admin@12345"
    hashed_password = get_password_hash(raw_password)
    assert hashed_password != raw_password
    assert bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
```

---

**Test Utilities**

- **Fixture**: `setup_db`

  - **Description**: Sets up and tears down the test database. It drops the `user` collection before the tests run and drops it again after the tests complete to ensure a clean state.

- **Function**: `create_user`

  - **Description**: Helper function to create a user in the database with a given email and password. It hashes the password using bcrypt and inserts the user document with a hardcoded id of 1.