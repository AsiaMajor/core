# CORE

## SETUP:
* `$ cd core`
* `$ virtualenv env`
* `$ source env/bin/activate`
* `$ pip3 install requirements.txt`
* `$ FLASK_DEBUG=1 flask run`

## Testing:
* `$ pytest -vv`

## API endpoints:
* `localhost:5000/` with method `GET` --> Frontend end-point.
* `localhost:5000/api/ping` with method `GET`
* `localhost:5000/api//analyze` with method `POST`
