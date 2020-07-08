import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from sqlalchemy import func
from werkzeug.exceptions import HTTPException
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance


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
def get_actors():
  try:
      all_actors = Actor.query.order_by(Actor.id).all()
      actors = [{"name": actor.name, "age": actor.age,
                       "gender": actor.gender}
                      for actor in all_actors]

      return jsonify({"sucess":True,"actors":actors})

  except Exception as e:
        logging.exception(e)
        abort(500)

@app.route('/actors', methods=['POST'])
def add_actor():
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

@app.route('/movies')
def get_movies():
    try:
        all_movies = Movie.query.order_by(Movie.id).all()

        movies = [{"title": movie.title, "release_date": movie.release_date}
                      for movie in all_movies]

        return jsonify({
            'success': True,
            'movies': movies,
        }), 200
    except Exception:
        abort(422)







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
