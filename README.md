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


## get_password_hash
This function takes a `password` string as input and returns the hashed password using `pwd_context.hash(password)`.

**Parameter:**

- `password`: A string.

**Returns:**

- The hashed password.

Please note that `Session`, `schemas.AdminUserBase`, `AdminUser`, and `pwd_context` are not defined in the given code. Make sure they are appropriately defined or imported in your actual code.


### Prerequisite 

To secure passwords, we're using the `passlib` library's `CryptContext`, which allows us to hash passwords.
Here, `bcrypt` hashing scheme is used. 

### Function: get_password_hash

`get_password_hash` is a function that takes a plain password as an argument and returns its hashed version. The `passlib` library's `hash` method is used to convert the plain password into a hashed version.

### verify_password
This function verifies if the plain, unhashed password matches the hashed password.

**Parameters:**

- `plain_password`: A string representing the plain, unhashed password.
- `hashed_password`: A string representing the hashed password.

**Returns:**

A boolean value indicating the result of the password verification check.


## authenticate_user
This function authenticates a user in a SQLAlchemy session database by comparing the name and verifying the password of the user.

**Parameters:**

- `db`: A SQLAlchemy session.
- `user`: An instance of `AdminUserBase` from the schemas.

**Returns:**

A boolean value indicating whether the user was successfully authenticated or not.

Please remember that `Session`, `schemas.AdminUserBase`, `AdminUser`, and `pwd_context` need to be appropriately defined or imported in your actual code.

## API Endpoints Description
List and describe each of the API endpoints.

## Error Handling
Explain how errors are handled in your application.

## Source Code
All source code is stored on GitHub at [GitHub Repository](YOUR REPO URL).

## Technologies Used
List all the technologies used in your project.
- FastAPI
- PostgreSQL
- Docker

## Sources
Cite any sources or references you've used in developing your project.