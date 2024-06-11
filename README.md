[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=004DF7&random=false&width=435&lines=Twitter-like+application)](https://git.io/typing-svg)

This Docker application is a web service for a **Twitter-like application** written in Python
using:
> FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, pytest

### It consists of several components:

- **Web Service (web)**: A container containing the main application code, including API routes, Pydantic schemas, services, and database models.
- **PostgreSQL Database (db)**: A container with a PostgreSQL database for storing application data, such as users, tweets, and media files.
- **Nginx**: A container with Nginx acting as a reverse proxy server that proxies requests to the web service and serves static files (e.g., uploaded media files).

To run the application, you need to create an .env file and populate it with the appropriate values.
```
HOST=0.0.0.0
PORT=8000
ENV=development # or production

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=

POSTGRES_HOST_TEST=
POSTGRES_PORT_TEST=
POSTGRES_NAME_TEST=
POSTGRES_USER_TEST=
POSTGRES_PASSWORD_TEST=
```

### The application structure is organised into modules for different components (routes, schemas, services, database models, etc.).

```
└── .
    └── .env
    └── .gitignore
    └── 📁alembic
        └── env.py
        └── README
        └── script.py.mako
        └── 📁versions
    └── alembic.ini
    └── 📁app
        └── 📁api
            └── 📁routes
                └── media_routes.py
                └── tweet_routes.py
                └── user_routes.py
            └── 📁schemas
                └── media_schema.py
                └── result.py
                └── tweet_schema.py
                └── user_schema.py
                └── __init__.py
        └── 📁core
            └── config.py
            └── __init__.py
        └── 📁db
            └── database.py
            └── __init__.py
            └── 📁models
                └── media_model.py
                └── tweet_model.py
                └── user_model.py
                └── __init__.py
        └── main.py
        └── __init__.py
        └── 📁services
            └── media_service.py
            └── tweet_service.py
            └── user_service.py
            └── __init__.py
        └── 📁utils
            └── utils.py
            └── __init__.py
    └── docker-compose.yml
    └── Dockerfile
    └── init_db.sh
    └── nginx.conf
    └── pytest.ini
    └── README.md
    └── requirements.txt
    └── run.py
    └── __init__.py
    └── 📁static
        └── 📁css
        └── favicon.ico
        └── index.html
        └── 📁js
    └── 📁tests
        └── conftest.py
        └── test_image.jpg
        └── test_media.py
        └── test_tweets.py
        └── test_users.py
        └── __init__.py
```

> In the app folder, create a media folder if it is not already there.

After running 
```
docker-compose up -d
```
the application will be available at http://localhost.

To initialize the database and add test data, you need to execute the init_db.sh scriptwhich is also linked to .env.
Run from the root of the project using the command
```
sh init_db.sh
```