# Project Name

## Introduction 
This is an fastapi api for school cafeteria for chipping lunches. 

## Use cases

### **Use Case: Creating a New User**
- **Description:** The administrator creates a new student user in the system.
- **Actor:** Administrator
- **Basic Flow of Events:**
  1. The administrator navigates to the user management area in the system.
  2. The administrator selects the option to create a new user.
  3. The system presents a form requesting necessary student details.
  4. The administrator enters the student's details into the form fields.
  5. The administrator submits the form.

### Use Case: Student Tag Scanning
- **Description:** The system scans the RFID tag as a student presents it.
- **Actor:** RFID scanner
- **Basic Flow of Events:**
  1. The student presents their card to the RFID scanner.
  2. The scanner reads and verifies the card data.
  3. The system retrieves the student's lunch number if has any.

### Use Case: Assigning Lunch to Student
- **Description:** The system assigns lunch to the student after validating their RFID card.
- **Actor:** Lunch assignment system.
- **Basic Flow of Events:**
  1. The system assigns a lunch to the student.
  2. The system logs the assignment in the student's account.


## Architecture Structure
Diagram and explanation of the architecture of your app.

## ERD (Entity Relationship Diagram)
![Alternative text for the image](/static/ERD.png)

## Authentication

### `create_admin_user`

This function creates an admin user in a given database.

**Parameters:**

- `db`: A SQLAlchemy session.
- `user`: An instance of `AdminUserBase` from the schemas.

**Returns:**

- `name`: Name of the newly added admin user.

This function starts by hashing the password, then creates a new instance of the `AdminUser` with the provided name and hashed password. This user is then added to the database with `db.add(db_user)`, and the changes are committed to the database with `db.commit()`. The new user is then refreshed and the username is returned.


### `get_password_hash`

`get_password_hash` is a function that takes a plain password as an argument and returns its hashed version. The `passlib` library's `hash` method is used to convert the plain password into a hashed version.

### `verify_password`
This function verifies if the plain, unhashed password matches the hashed password.

**Parameters:**

- `plain_password`: A string representing the plain, unhashed password.
- `hashed_password`: A string representing the hashed password.

**Returns:**

A boolean value indicating the result of the password verification check.


### `authenticate_user`
This function authenticates a user in a SQLAlchemy session database by comparing the name and verifying the password of the user.

**Parameters:**

- `db`: A SQLAlchemy session.
- `user`: An instance of `AdminUserBase` from the schemas.

**Returns:**

A boolean value indicating whether the user was successfully authenticated or not.

Please remember that `Session`, `schemas.AdminUserBase`, `AdminUser`, and `pwd_context` need to be appropriately defined or imported in your actual code.

## API Endpoints Description

### POST /users
This endpoint creates a new user in the database. 

**Request Body:**

- `user`: An instance of `UserBase` from the schemas.

**Returns:**

The name of the newly created user.

### PUT /users/{user_name}/lunches/{type_of_lunch}
This endpoint updates a user's lunch in the database.

**Parameters:**

- `user_name`: A string representing the username.
- `type_of_lunch`: An integer representing the type of lunch. The valid range is from 0 to 3, inclusive.
- `db`: A SQLAlchemy session.

**Returns:**

A Boolean value indicating the success of the operation.

### GET /users/total
This endpoint retrieves the total count of users in the database.

**Request Parameters:**

None

**Returns:**

An integer value representing the total count of users in the database.

### GET /users/lunch
This endpoint retrieves all users from the database who have either lunch_out 1 or 2 and type_of_lunch 1, 2 or 3.

**Request Parameters:**

None

**Returns:**

A list of user instances where each instance represents a user who satisfies the given lunch conditions. If no users satisfy these conditions, the endpoint returns zero.

### GET /users/{user_id}
This endpoint retrieves a specific user from the database by `user_id`. If the user has any lunch records, it will also update the `lunch_out` field of the user's lunch record by following rules:

If `lunch_out` is 0, it will be updated to 1.
If `lunch_out` is 1, it will be updated to 2.

**Path Parameters:**

- `user_id`: The ID of the user to lookup in the database.

**Returns:**

An instance of the looked-up user if found, along with updated lunch records if any. If the user is not found, the endpoint returns zero. If updating the `lunch_out` field fails, it raises an HTTP 500 error with the detail "Failed to update lunch_out".

### GET /users/{user_id}/name
This endpoint retrieves the name of a specific user given the `user_id`.

**Path Parameters:**

- `user_id`: The ID of the user whose name is to be retrieved.

**Returns:**

The name of the user if found. If no user is found with the provided `user_id`, the endpoint would return None.

### GET /users/lunch/out
This endpoint retrieves the count of lunches where `lunch_out` and `type_of_lunch` are greater than zero.

**Request Parameters:**

None

**Returns:**

An integer value representing the count of lunches where `lunch_out` and `type_of_lunch` are greater than zero.

### GET /lunches/rest/total
This endpoint retrieves the total number of lunches in the database with `type_of_lunch` greater than zero but not marked as `lunch_out` (where `lunch_out` is also greater than zero).

**Request Parameters:**

None

**Returns:**

An integer value representing the count of lunches in the database with `type_of_lunch` greater than zero but not marked as `lunch_out`.

### GET /lunches/out/total
This endpoint retrieves the total number of lunches with `lunch_out` and `type_of_lunch` greater than zero.

**Request Parameters:**

None

**Returns:**

An integer value representing the count of lunches where `lunch_out` and `type_of_lunch` are greater than zero.

### DELETE /users
This endpoint deletes all users from the database. It also deletes all related lunch records for each deleted user.

**Request Parameters:**

None

**Responses:**

- If the operation is successful, it does not return any content with a HTTP status code 204.
- If there is an error during the operation, it will throw the respective exception with relevant details.

### DELETE /users/{user_id}
This endpoint deletes a specific user from the database using a `user_id`. It also deletes the lunch record associated with the user.

**Path Parameters:**

- `user_id`: The ID of the user to be deleted.

**Responses:**

- The name of the user that was deleted is returned if the operation is successful.
- If there is an error during the operation, it will throw the respective exception with relevant details.

### DELETE /users/grade/{grade}
This endpoint deletes users from the database based on their grade. It also deletes all related lunch records for each deleted user.

**Path Parameters:**

- `grade`: The grade of the users to be deleted.

**Responses:**

- The grade of the users that were deleted is returned if the operation is successful.
- If there is an error during the operation, it will throw the respective exception with relevant details.

## Error Handling
1. **HTTPException:** The FastAPI `HTTPException` is raised whenever an exceptional situation occurs. This carries an HTTP status code and a detail message to describe the issue. For instance, if the requested user does not exist, a `HTTPException` is raised with status code 404 and detail message "User not found". Similarly, if an invalid `type_of_lunch` is provided (i.e., less than 0 or greater than 3), another `HTTPException` is raised with a 404 status code and an "Invalid type of lunch" detail message.

2. **Database Operations:** The function tries to execute database operations. If any exception occurs during this process (e.g., trying to modify a lunch that does not exist), the operations are wrapped in a `try/except` block. In case an error occurs, the database operations are rolled back to the state before the operations began and the respective `HTTPException` is raised.

## Source Code
All source code is stored on GitHub at [GitHub Repository](YOUR REPO URL).

## Technologies Used
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker

## Sources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [AUTH in fastapi](https://www.fastapitutorial.com/blog/authentication-in-fastapi/)