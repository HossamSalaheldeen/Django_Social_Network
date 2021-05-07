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


### As a user you can  
```
- register myself in social media app
- login to the social media app
- add friends 
- edit my profile 
- create post
- can join groups
- like friends posts and comment on any friend's post
- delete my posts only
- delete my comments only
- unlike posts
- visit my friends profile 
- can create a group 
- receive a group join request if I am a group owner
- sent a join request to a specific group
- search for any group name 
- send a message to any of my friends list through email
- see my notifications through email

```
##### As an Admin you can
```
- can deactiviate user
- edit groups members 
- remove any group with all its related data
- As an admiin I can create/edit Profanities List (Bad words list) that will validate the accepatnce of posts and comments 

```
