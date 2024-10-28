# StarNavi FastAPI

A simple API for managing posts and comments with AI moderation and automated replies. 
The API was developed using FastAPI and Pydantic. Perform basic social media actions.
Analytics on the number of comments added to posts over a certain period.

## Table of Contents

- [Task](#task)
- [Installation](#installation)
- [Launch periodic task with Celery](#launch-periodic-task-with-celery)
- [Run with docker](#run-with-docker)
- [Run tests](#run-tests)
- [Getting access](#getting-access)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [General Features](#general-features)
- [DB Structure](#db-structure)
- [An example of using the API](#an-example-of-using-the-api)

## Task

Нижче описано перелік функцій які повинні бути імплементовані:

- Реєстрація користувачів;

- Вхід користувачів;

- API для управління постами;

- API для управління коментарями;

- Перевірка поста чи коментарів в момент створення на наявність нецензурної лексики, образ тощо, та блокування таких постів чи коментарів.

- Аналітика щодо кількості коментарів, які були додані до постів за певний період. Приклад URL: /api/comments-daily-breakdown?date_from=2020-02-02&date_to=2022-02-15. API має повертати аналітику, агреговану по днях за кожен день, повинно повернутись кількість створених коментарів і кількість заблокованих.

- Функція автоматичної відповіді на коментарі якщо це увімкнув користувач для своїх постів. Автоматична відповідь повинна відбуватись не одразу, а через проміжок часу який налаштує користувач. Також відповідь повинна бути релевантна до поста та коментаря на який відбувається відповідь.

* Важливою умовою є те що мають бути написані тести до таких функцій як створення постів, та аналітика. Наявність тести для всіх функції буде плюсом.

- Покрити код тестами

## Installation

```bash
git clone https://github.com/AlexTsikhun/starnavi_fastapi
cd starnavi_fastapi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# set env variables
alembic revision --autogenerate -m "Init"
alembic upgrade head
python3 -m uvicorn main:app --reload
```
## Launch periodic task with Celery

Celery should be installed locally. Run worker and flower:

```bash
celery -A celery_app worker --loglevel=info

celery -A celery_app flower --port=5555
```

Gemini APi not allowed in Ukraine, so I used VPN. Run OpenVNP:

```
sudo openvpn vpnbook-us16-tcp443.ovpn
# username - vpnbook
# pass- b6xnvt9 
```

## Run with docker

Docker should be installed locally

```bash
docker compose build
docker compose up
```

## Run tests

Add path to `.env` files for test configuration

```bash
pytest tests/
```
## Getting access

- Create user via `api/v1/user/register/`
- Get access token `api/v1/user/token/`
- API Root `api/v1/posts/`

## Technologies Used

- FastAPI, Pydantic
- Celery, Redis
- Sqlite3
- Docker, docker compose
- Unittest

## Features:

- schedule Comment answer with Celery (You can set the time for an automatic response)
- automatic Comment answer with Gemini API (To better maintain the logic of the questions and answers, you can use `model.start_chat`)
- profanity checker with Gemini API (because profanity-checker library does not work 
with languages other than English, LLM transformers are too computationally complex for this task)
- JWT authenticated
- Documentation is located at `docs`
- Managing Posts and Comments
- Pagination for Posts

### General Features

User Registration and Authentication:

- Users can register with their email and password to create an account.

- Users can log in with their credentials and receive a token for authentication.

- Users can log out and invalidate their token.

Post/Comment Creation and Retrieval:

- Users can create new posts/comment with text content (if the text contains profanity - blocking)

- Analytics on the number of comments added to posts over a certain period.

Schedule Post creation using Celery:

- Added possibility to schedule Post creation (you can select the time to create the Post before creating of it).

API Permissions:

- Only authenticated users can perform actions such as creating/updating/deleting posts/comments.

API Documentation:

- The API is well-documented with clear instructions on how to use each endpoint.

- The documentation is included sample API requests and responses for different endpoints.

Technical Requirements:

- Used Django and Django REST framework to build the API.

- Used JWT authentication for user authentication.

- Used appropriate schemas for data validation and representation.

- Used appropriate URL routing for different API endpoints.

- Followed best practices for RESTful API design and documentation.

#### DB Structure:

![db_structure.png](images/db_structure.png)

### An example of using the API

A list of some of the main-simples endpoints (for more, use documentation):

registration:

![registration.png](images/registration.png)

Not authenticated:

![not_authenticated_attempt.png](images/not_authenticated_attempt.png)

login_get_token:

![login_get_token.png](images/login_get_token.png)

me:

![me.png](images/me.png)

post_creation:

![post_creation.png](images/post_creation.png)


post_creation_with_profanity:

![post_creation_with_profanity.png](images/post_creation_with_profanity.png)


comment_creation:

![comment_creation.png](images/comment_creation.png)


comment_creation_with_profanity:

![comment_creation_with_profanity.png](images/comment_creation_with_profanity.png)


stats:

![stats.png](images/stats.png)

comment_autoreply:

![comment_autoreply.png](images/comment_autoreply.png)


delete_post:

![delete_post.png](images/delete_post.png)


<details style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px">
<summary style="font-size: 1.17em; font-weight: bold; ">Future work</summary>

- Add roles
- More validation to creation process
- use gemini chat
- mocks in tests
- respond to a specific message
</details>
