# Flask Boilerplate

[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)](LICENSE)

  Flask Boilerplate to quickly get started with production grade flask application with some additional packages and configuration prebuilt.


# Getting Started

### Prerequisites

- Python 3.11.3 or higher
- Up and running Redis client

### Project setup
```sh
# clone the repo
$ git clone https://github.com/smit271/flask-prod-boilerplate.git
# move to the project folder
$ cd flask-prod-boilerplate
```
If you want to install redis via docker
```sh
$ docker run -d --name="flask-boilerplate-redis" -p 6379:6379 redis
```

### Creating virtual environment

- Install `pipenv` a global python project `pip install pipenv`
- Create a `virtual environment` for this project
```shell
# creating pipenv environment for python 3
$ pipenv --three
# activating the pipenv environment
$ pipenv shell
# install all dependencies (include -d for installing dev dependencies)
$ pipenv install -d

# if you have multiple python 3 versions installed then
$ pipenv install -d --python 3.11
```
### Configuration

- There are 3 configurations `development`, `staging` and `production` in `config.py`. Default is `development`
- Create a `.env` file from `.env.example` and set appropriate environment variables before running the project

### Running app

- Run flask app `python run.py`
- Logs would be generated under `log` folder

### Running celery workers

- Run redis locally before running celery worker
- Celery worker can be started with following command
```sh
# run following command in a separate terminal
$ celery -A celery_worker.celery worker --loglevel='INFO'  
# (append `--pool=solo` for windows)
```


# Preconfigured Packages
Includes preconfigured packages to kick start flask app by just setting appropriate configuration.

| Package 	| Usage 	|
|-----	|-----	|
| [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) 	| Running background tasks 	|
| [redis](https://redislabs.com/lp/python-redis/) 	| A Python Redis client for caching 	|
| [flask-cors](https://flask-cors.readthedocs.io/) 	| Configuring CORS 	|
| [python-dotenv](https://pypi.org/project/python-dotenv/) 	| Reads the key-value pair from .env file and adds them to environment variable. 	|
| [marshmallow](https://marshmallow.readthedocs.io/en/stable/) 	| A package for creating Schema, serialization, deserialization 	|
| [webargs](https://webargs.readthedocs.io/) 	| A Python library for parsing and validating HTTP request objects 	|

`autopep8` & `flake8` as `dev` packages for `linting and formatting`

# Test
  Test if this app has been installed correctly and it is working via following curl commands (or use in Postman)
- Check if the app is running via `status` API
```shell
$ curl --location --request GET 'http://localhost:5000/status'
```
- Check if core app API and celery task is working via
```shell
$ curl --location --request GET 'http://localhost:5000/api/v1/test_app/test-route'
```

# License
 This program is free software under MIT license. Please see the [LICENSE](LICENSE) file in our repository for the full text.