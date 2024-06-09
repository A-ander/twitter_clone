#!/bin/bash

# Initialize the database using Alembic
docker exec -it twitter alembic revision --autogenerate -m "init"
docker exec -it twitter alembic upgrade head

# Insert the test data
docker exec -it postgres_db psql -U postgres -d postgres -c "INSERT INTO users (name, api_key) VALUES ('Test User', 'test_key');"
docker exec -it postgres_db psql -U postgres -d postgres -c "INSERT INTO users (name, api_key) VALUES ('Test1', 'test');"
docker exec -it postgres_db psql -U postgres -d postgres -c "INSERT INTO user_followers (follower_id, followed_id) VALUES (1, 2);"
docker exec -it postgres_db psql -U postgres -d postgres -c "INSERT INTO user_followers (follower_id, followed_id) VALUES (2, 1);"