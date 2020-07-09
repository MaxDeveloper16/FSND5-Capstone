import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from sqlalchemy import func
from werkzeug.exceptions import HTTPException
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance
from auth.auth import AuthError, requires_auth



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(filename="api.log", level=logging.ERROR)

@app.after_request
def after_request(response):
    """Modify response headers including Access-Control-* headers.

    :param response: An instance of the response object.
    :return: As instance of the response object with Access-Control-* headers.
    """
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
    )
    return response

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
  try:
      all_actors = Actor.query.order_by(Actor.id).all()
      actors = [{"id":actor.id,"name": actor.name, "age": actor.age,
                       "gender": actor.gender}
                      for actor in all_actors]

      return jsonify({"success":True,"actors":actors})

  except Exception as e:
        logging.exception(e)
        abort(500)

@app.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def add_actor(payload):
    data = request.get_json()
    name = data.get("name", None)
    gender = data.get("gender", None)
    age = data.get("age", None)

    if not all([name, gender, age]):
      abort(400)

    try:
        new_actor = Actor(
          name=name,
          gender=gender,
          age=age
        )
        new_actor.insert()

        return jsonify(new_actor.format()), 201
    except Exception as e:
        logging.exception(e)
        abort(500)

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(payload, actor_id):

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400)

    new_name = data.get('name')
    new_age = data.get('age')
    new_gender = data.get('gender')

    try:
        if new_name is not None:
            actor.name = new_name

        if new_gender is not None:
            actor.gender = new_gender

        if new_age is not None:
            actor.age = new_age

        actor.update()

        new_actor = [actor.format()]

        return jsonify({
            'success': True,
            'actor': new_actor,
        }), 200

    except Exception:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload, actor_id):

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        'success': True,
        'delete': actor_id,
    }), 200


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    try:
        all_movies = Movie.query.order_by(Movie.id).all()

        movies = [{"id":movie.id,"title": movie.title, "release_date": movie.release_date}
                      for movie in all_movies]

        return jsonify({
            'success': True,
            'movies': movies,
        }), 200
    except Exception:
        abort(422)

@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def add_movies(payload):
    data = request.get_json()
    title = data.get("title", None)
    release_date = data.get("release_date", None)

    if not all([title, release_date]):
      abort(400)

    try:
        new_movie = Movie(
          title=title,
          release_date=release_date
        )
        new_movie.insert()

        return jsonify(new_movie.format()), 201
    except Exception as e:
        logging.exception(e)
        abort(500)

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(payload, movie_id):

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400)

    new_title = data.get('title')
    new_release_date = data.get('release_date')

    try:
        if new_title is not None:
            movie.title = new_title

        if new_release_date is not None:
            movie.release_date = new_release_date

        movie.update()

        new_movie = [movie.format()]

        return jsonify({
            'success': True,
            'movie': new_movie,
        }), 200

    except Exception:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_moive(payload, movie_id):

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    movie.delete()

    return jsonify({
        'success': True,
        'delete': movie_id,
    }), 200


## Error Handling
'''
Implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

@app.errorhandler(500)
def unknown(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Unknown server error"
    }), 500

@app.errorhandler(AuthError)
def authentification_failed(AuthError): 
    return jsonify({
        "success": False, 
        "error": AuthError.status_code,
        "message": AuthError.error['description']
        }), AuthError.status_code




#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
