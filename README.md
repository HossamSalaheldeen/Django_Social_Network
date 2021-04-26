# Social Media application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/HossamSalaheldeen/Django_Social_Network.git
$ cd Django_Social_Network
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3.8 env
$ .\env\Scripts\activate (for windows)
$ source env/bin/activate (for linux)
```

```sh
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd Django_Social_Network
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.
