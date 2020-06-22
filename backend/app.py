import os
import sys
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movies, Actors, setup_db, db
from sys import exc_info

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,-Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                        'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/', methods=['GET'])
  def print_hello():
    return jsonify('Right Endpoint')

  @app.route('/movies', methods=['GET'])
  def show_movies():
    error = False
    try:
      movies = Movies.query.all()
      formated = [movie.format() for movie in movies]

      return jsonify({
        "success":True,
        "movies": formated
      })
    except Exception:
      error = True
      db.session.rollback()
      print(exc_info())
    finally:
      db.session.close()
      if error:
        abort(500)

  @app.route('/actors', methods=['GET'])
  def show_actors():
    error = False
    try:
      actors = Actors.query.all()
      formated = [actor.format() for actor in actors]

      return jsonify({
        "success":True,
        "actors": formated
      })
    except Exception:
      error = True
      db.session.rollback()
      print(exc_info())
    finally:
      db.session.close()
      if error:
        abort(500)

  @app.route("/movies", methods=['POST'])
  def add_movies():
    data = request.json
    try:
      if data["title"] and data["release_date"]:
        title = data["title"]
        release_date = data["release_date"]
        movie = Movies(title=title,release_date=release_date)
        movie.insert()

        return jsonify({
          "success":True,
          "movie":movie.id
        })
      else:
        abort(422)
    except Exception:
      db.session.rollback()
      print(exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/actors', methods=['POST'])
  def add_actors():
    data = request.json
    name = data["name"]
    age = data["age"]
    gender = data["gender"]
    actor = Actors(name=name,age=age,gender=gender)
    actor.insert()
    return jsonify({
      "success":True,
      "actor":actor.id
    })
  @app.route("/movies/<movie_id>", methods=['DELETE'])
  def delete_movies(movie_id):
    try:
      movie = Movies.query.get(movie_id)
      if movie:
        movie.delete()
        return jsonify({
          "success": True,
          "movie": movie.id
        })
      else:
        abort(404)
    except Exception:
      db.session.rollback()
      print(exc_info())
      abort(404)
    finally:
      db.session.close()

  @app.route("/actors/<actor_id>", methods=['DELETE'])
  def delete_actors(actor_id):
    try:
      actor = Actors.query.get(actor_id)
      if actor:
        actor.delete()
        return jsonify({
          "success":True,
          "actor":actor.id
        })
      else:
        abort(404)
    except Exception:
      db.session.rollback()
      print(exc_info())
      abort(404)
    finally:
      db.session.close()

  # @app.route("/movies/<movie_id>", methods=['PATCH'])
  # def update_movies():
  #   data = request.json
  #   return jsonify({
  #     "success":True,
  #     "movie":movie
  #   })
  # @app.route("/actors/<actor_id>", methods=['PATCH'])
  # def update_actors():
  #   data = request.json
  #   return jsonify({
  #     "success":True,
  #     "actor":actor
  #   })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "status code": 404,
      "message": "Sorry, resource unavailable"
    }), 404
  
  @app.errorhandler(422)
  def unproccesable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Sorry, request cannot be processed"
    }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "status code": 400,
      "message": "Sorry, Bad request"
    }), 400
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "status code": 500,
      "message": "Internal Server error"
    }), 500

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)