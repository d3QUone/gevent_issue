# Demo

Using Python 3.8.3

Install pipenv:
``` 
python3.8 -m pip install pipenv==2020.6.2
```

Install requirements:
```
pipenv install --dev
```

Run demo:
```
pipenv run uwsgi --ini src/uwsgi.ini
```

Sample URLs:
```
curl http://localhost:8110/
curl http://localhost:8110/status
```

## Using Docker

Install Docker (using official docs). 

Run with Docker: 
```
make build_app
make run_app
```
