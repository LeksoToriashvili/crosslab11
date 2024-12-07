# crosslab11
# Developing stay connected app  with crosslab11 group

## Django Q&A Platform API
This project is a Django-based REST API for a Question-and-Answer (Q&A) platform.
It allow users to register, post questions, provide answers, interact with content via tags and likes.
The platform also supports user ratings and statistics. 

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
5. [Models Overview](#models-overview)
6. [Permissions](#permissions)
7. [Dependencies](#dependencies)
8. [Contributors](#contributors)

## Features

- Secure User Authentication using JWT tokens
- Endpoints to obtain, refresh and verify tokens for session management
- CRUD operations for managing user accounts
- Quiz management
- Interactive API Documentation with Swagger UI


## Installation

### requirements:
- Django==5.1.3
- djangorestframework==3.15.2 (DRF)
- djangorestframework-simplejwt==5.3.1 (JWT)
- A Database (Mysql)

### Steps

1. Clone the repository:
```bash

git clone https://github.com/LeksoToriashvili/crosslab11
cd project-directory
```

2. install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser
```bash
python manage.py createsuperuser
```

5. Start the development server
```bash
python manage.py runserver
```


## Usage

1. Register or log in to interact with the API
2. Use endpoints to create and retrieve questions, answers, tags and likes
3. Filter and search questions using parameters like, tags, keywords and etc

# API Endpoints

1. Authentication
```bash
Obtain Token

    Endpoint: POST /api/token/
    Description: Used to generate access and refresh tokens
    Request Payload:
    {
        "username":"<username>",
        "password":"<password>"
    }

    Response:
    {
        "access":"<access_token>",
        "refresh":"<refresh_token>"
    }


Refresh Token

    Endpoint: POST /api/token/refresh/
    Description: Used to refresh access token using a valid refresh token
    Request Payload:
    {
        "refresh":"<refresh_token>"    
    }

    Response:
    {
        "access":"<access_token>",
    }


2. User Management (Accounts)

Registration

    Endpoint: POST /api/account/
    Description: Creates a new user
    Request Payload:
    {
        "username": "<username>",
        "email": "<email>",
        "password": "<password>"
    }  


Retrieve User/Users

    Endpoint 1: GET /api/account/
    Description: Retrieve a list of all registered users.

    Endpoint 2: GET /api/account/{id}/
    Description: Retrieve details of a specific user by ID.

    p.s. use PUT, or DELETE methods if you want update, or delete a specific user

```

2. Quiz Management (Core)
- Question Endpoints
```bash

List Questions

    Endpoint: GET /api/questions/

    Description: Retrieve a list of all questions.

Retrieve Question

    Endpoint: GET /api/questions/{id}/

    Description: Retrieve details of a specific question by ID.

Create Question

    Endpoint: POST /api/questions/

    Description: Add a new question.

    Request Payload:

    {
        "text": "<question_text>",
        "category": "<category_id>"
    }

Update Question

    Endpoint: PUT /api/questions/{id}/

    Description: Update an existing question.

Delete Question

    Endpoint: DELETE /api/questions/{id}/

    Description: Remove a specific question.

```

3. Answer Management(Core)
- Answer endpoints
```bash
Create answer

    Endpoint: POST /api/answers/
    Description: create answer to a specific question

    Request Payload:

        {
            "text": "<answer_text>",
            "question": "<question_id>"
        }

Retrieve all answers of a specific question

    Endpoint: GET /api/answers/by_question/{question_id}
    Description: retrieves all answers of a specific question

Mark answer as accepted
    Endpoints: POST /api/answers/{answer_id}/mark_accepted/
    Description: 

```

4. Like Management (Core)
```bash
Like an answer

    Endpoint: POST api/likes/
    Description: adds like to a specific answer, which's id is in the request
    Request Payload:
    {
        "answer": 12
    }

Unlike an answer (remove)

    Endpoint: DELETE /api/likes/{answer_id}/remove_like/
    Description: removes your like while you are authorized

Retrieve all likes of a specific answer
    Endpoint: GET /api/likes/{answer_id}/likes-count/
    Description: removes your like while you are authorized

```

5. User Rating management
```bash
    Endpoint: POST /api/rating/
    Description: Retrieves user's calculated rating according to total answers and amount of liked answers
    Request Payload:
    {
        "username":"<username>"
    }
```

6. User Statistics management
```bash
    Endpoint: POST api/answers-count/
    Description: Retrieves user's username, answer count and user's total likes
    Request Payload:
    {
        "id":{user_id}
    }

```

## Debugging
- Debug Toolbar


## API Documentation
1. Swagger UI
    - Endpoint: /
    - Description: View the interactive API Documentation generated by Swagger


Notes

- All endpoints related to POST, PUT, or DELETE actions require authentication using a valid JWT token.

- Use /api/token/ to obtain tokens for authenticated access

## Contributors
- **Lekso Toriashvili** [GitHub](https://github.com/LeksoToriashvili)
- **Mariam Gaprindashvili** [GitHub](https://github.com/MarBifrost)

---

Thank you for your interest in this project! 
If you have any suggestions or ideas, feel free to submit an issue or a pull request. 
Happy coding! 😊


