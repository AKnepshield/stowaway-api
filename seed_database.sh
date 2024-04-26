#!/bin/bash

rm db.sqlite3
rm -rf ./stowawayapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations stowawayapi
python3 manage.py migrate stowawayapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata condition
python3 manage.py loaddata records

