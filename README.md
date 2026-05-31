# ToDo API Project

A project inspired by [roadmap.sh](https://roadmap.sh/projects/todo-list-api) that creates a RESTful API that allows **authenticated** users to create and manage their ToDo lists and items.

It was created using django and django-rest-framework (DRF)

## Setup

1. Clone the Repository

```bash
  git clone https://github.com/OveaTrint/to-do-api.git
  cd to-do-api
```

2. Install and sync dependencies and activate the virtual environment

```bash
  uv sync
  source .venv/Scripts/activate
```

3. Make sure you have set your secret and database credentials in an `.env` file

```env
SECRET_KEY="YOUR SECRET KEY"
DATABSE_PW="YOUR_PW"
...
...
```

Make sure to create the database before migrating if using postgres.

4. Migrate the database

```bash
  python manage.py makemigrations
  python migrate
```

5. (Optional) Generate schema for swagger

```bash
 ./manage.py spectacular --color --file schema.yml
```

6. Start the server

```bash
  python manage.py runserver
```

## API Endpoints

### Authentication

`/register`

- Method: `POST`
- Description: Registers a user
- Request Body:

```json
{
  "username": "Random user",
  "email": "random@gmail.com",
  "password": "randomuserpassword"
}
```

- Response

```json
{
  "access": "your.jwt.aceess-token",
  "refresh": "your.jwt.refresh-token"
}
```

- `200 Created` if user is created successfully
- `400 Bad Request` if request data is invalid or user credentials already exist in the database

`/login`

- Method: `POST`
- Description: Authenticates a user
- Request Body:

```json
{
  "email": "random@gmail.com",
  "password": "randomuserpassword"
}
```

- Response

```json
{
  "access": "your.jwt.aceess-token",
  "refresh": "your.jwt.refresh-token"
}
```

- `200 OK` if user is authenticated successfully
- `400 Bad Request` if request data is invalid or user credentials already exist in the database

### ToDos

**All requests sent here require the `Authorizaton: Bearer <access_token>` to be set**

`/todos`

- Method: `GET`
- Description: Gets all todos of a specific user
- Query Parameters:
    - `limit` (optional): The maximum number of items retrievable at once
    - `offset` (optional): The starting position of the retrieved items

- Response

```json
{
  "count": 1023,
  "next": "https://localhost:8000/todos?limit=100&offset=500",
  "previous": "https://localhost:8000/todos?limit=100&offset=300",
  "results": [
    {
      "id": 401,
      "title": "Shopping",
      "description": "Buy bread, eggs and milk"
    },
    ...
    ...
  ]
}
```

- `200 OK` when items are retrieved successfully

`/todos`

- Method: `POST`
- Description: Creates a ToDo Item
- Request Body:

```json
{
  "title": "Shopping",
  "description": "Buy bread, eggs and milk"
}
```

- Response

```json
{
  "id": 1,
  "title": "Shopping",
  "description": "Buy bread, eggs and milk"
}
```

- `201 Created` if todo item is created successfully
- `400 Bad Request` if request data is invalid

`/todos/{id}`

- Method: `PUT`
- Description: Updates a ToDo Item
- Request Body:

```json
{
  "title": "Shopping",
  "description": "Buy bread, eggs and milk. I almost forgot sausages"
}
```

- Response

```json
{
  "id": 1,
  "title": "Shopping",
  "description": "Buy bread, eggs and milk. I almost forgot sausages"
}
```

- `200 OK` if todo item is updated successfully
- `400 Bad Request` if request data is invalid
- `404 Does not exist` if todo item doesn't exist

`/todos/{id}`

- Method: `DELETE`
- Description: Deletes a ToDo Item

- `204 No Content` if todo item is updated successfully
- `404 Does not exist` if todo item doesn't exist

### Refresh tokens

Access tokens can be refreshed after they expire using your refresh token.

`api/token/refresh`

- Method: `POST`
- Request Body

```json
  {
  "refresh": "your.refresh.token"
}
```

- Response Body

```json
  {
  "access": "your.access.token"
}
```

### Throttling and Rate-limiting

These are impelemented via the `rest_framework.throttling.AnonRateThrottle` and
`rest_framework.throttling.UserRateThrottle` classes provided by DRF

To change the limit, go to the `settings.py` module in the `to_do_api` directory and edit the following excerpt

```python
...
"DEFAULT_THROTTLE_RATES": {
    "anon": "25/minute",
    "user": "50/minute"
}
```
