# Casting Agency Capstone Project For Udacity Full Stack Web Nanodegree Program

**Heroku link:** (https://fsnd-kang-capstone.herokuapp.com/)

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in api.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Running the server

To run the server, execute:

```bash
export FLASK_APP=myapp
export FLASK_ENV=debug
flask run --reload
```


## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models

### Actors
- name
- gender
- age

### Movies 
- title
- release_date

### Performance 
- actors.id 
- movies.id 
- actor_fee


## Environment Variables

In the `config.py` file, the JWT token for each User Role
- Casting Assistant
- Casting Director
- Executive Producer

## Roles

### Casting Assistant

- get:actors
- get:movies

### Casting Director
#####  All permissions a Casting Assistant has
- post:actor
- patch:actor
- delete:actor
- patch:movie

### Executive Producer

##### All permissions a Casting Director has
- post:movie
- delete:movie

## Endpoints

### GET '/actors'

```bash
{
    "actors": [
        {
            "id": 1,
            "name": "Jack",
            "age": 25,
            "gender": "Male"
        }
    ],
    "success": true
}
```

### POST '/actors'

```bash
{
    "id": 2,
    "name": "Lucy",
    "age": 28,
    "gender": "Female",
    
}
```


### PATCH '/actors/<int:actor_id>'

```bash
{
    "actor": [
        {
            "id": 1,
            "name": "Jack",
            "age": 25,
            "gender": "Male"          
        }
    ],
    "success": true
}
```

### DELETE '/actors/<int:actor_id>'

```bash
{
    "delete": 1,
    "success": true
}
```

### GET '/movies'

```bash
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 01 Oct 2020 00:00:00 GMT",
            "title": "X-War"
        }
    ],
    "success": true
}
```

### POST '/movies'

```bash
{
    "id": 2,
    "release_date": "Wed, 08 Jul 2020 00:00:00 GMT",
    "title": "New Movie"
}
```

### PATCH '/movies/<int:movie_id>'

```bash
{
    "movie": [
        {
            "id": 1,
            "release_date": "Thu, 01 Oct 2020 00:00:00 GMT",
            "title": "X-War"
        }
    ],
    "success": true
}
```


### DELETE '/movies/<int:movie_id>'

```bash
{
    "delete": 1,
    "success": true
}
```

## Testing

To run the tests in your terminal

```bash

pytest test_app.py
```

## Testing endpoint with postman

Import the postman collection `FSDN-Capstone.postman_collection.json`
 
Running Collections with Heroku URL to test endpoint.
