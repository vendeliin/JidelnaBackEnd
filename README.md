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
Describe how authentication is handled in your project.

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