# CORE

## SETUP:
* Assuming you have `psql`
1. `$ psql`
2. `psql==> CREATE DATABASE asiamajor`
3. `psql==> \q`
4. `$ python3 manage.py db init`
5. `$ python3 manage.py db migrate`
6. `$ python3 manage.py db upgrade`

## How to run:
* `$ cd core`
* `$ pip3 install flask flask_restful`
* `$ FLASK_APP=app.py FLASK_DEBUG=1 flask run`

## How to update database:
* `$ python3 manage.py db migrate`
* `$ python3 manage.py db upgrade`

## API endpoints:
* `localhost:5000/api/v1/all` with method `GET`
* `localhost:5000/api/v1/analyze` with method `POST`