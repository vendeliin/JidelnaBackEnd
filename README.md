# FastAPI Application

This is a FastAPI application that provides an API for user and lunch management.

## Endpoints Documentation

### Create a User

- URL: `/create/user`
- Method: `POST`
- Body: `user` object
- Response: Creates a new user

### Log In

- URL: `/login`
- Method: `POST`
- Body: `AdminUserBase` object
- Response: Authenticates a user

### Create Admin User

- URL: `/create/admin`
- Method: `POST`
- Body: `AdminUserBase` object
- Response: Creates a new admin user

### Update User Lunch

- URL: `/user/{user_name}/update-lunch/{type_of_lunch}`
- Method: `PUT`
- Parameters: `user_name` (string), `type_of_lunch` (int)
- Response: Updates the lunch type for a user

### Get User by ID

- URL: `/user/{user_id}`
- Method: `GET`
- Parameters: `user_id` (string)
- Response: Returns information of a user by ID

### Get Lunch Out Users

- URL: `/users/WithLunchOut`
- Method: `GET`
- Response: Returns users having lunch out 

### Get All Users

- URL: `/users/All`
- Method: `GET`
- Response: Returns all users 

### Get Users Count

- URL: `/users/count`
- Method: `GET`
- Response: Returns the number of users 

### Get Lunches Count at Restaurant

- URL: `/lunches/count/rest`
- Method: `GET`
- Response: Returns the count of lunches at the restaurant 

### Get User Name

- URL: `/user/name/{user_id}`
- Method: `GET`
- Parameters: `user_id` (string)
- Response: Returns the name of a user

### Get Lunches Count Out

- URL: `/lunches/count/out`
- Method: `GET`
- Response: Returns the count of lunches out 

### Delete All Users

- URL: `/users/delete`
- Method: `DELETE`
- Response: Deletes all users 

### Delete User

- URL: `/user/delete/{user_id}`
- Method: `DELETE`
- Parameters: `user_id` (string)
- Response: Deletes a user 

### Delete Users by Grade

- URL: `/user/delete/by/grade/{grade}`
- Method: `DELETE`
- Parameters: `grade` (int)
- Response: Deletes users of a specific grade