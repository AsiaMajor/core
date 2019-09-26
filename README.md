<h1 align='center'>
    <strong>CORE</strong>
</h1>

<h3 align='center'>
    <strong>AsiaMajor's Code Repository</strong><br>
    Better, stronger, faster. Metriguard's gonna love this.
</h3>

We are in a mission to detect a veneer sheet in 0.5 seconds. We develop:
- Veneer fingerprint
- Fingerprint search algorithm

## SETUP:
```console
$ git clone https://github.com/AsiaMajor/core
$ cd core/
$ virtualenv env && source env/bin/activate
$ pip install requirements.txt
$ FLASK_APP=app.py FLASK_DEBUG=1 flask run
```

## API endpoints:
* `/api/ping` with method `GET`
* `/api/analyze` with method `POST`

## Team:
- @YukaLangbuana
- @Cfurukawa6
- @Bjpark4002
- @lampoon2gn
