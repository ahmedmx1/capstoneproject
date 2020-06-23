import os
import sys
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_cors import CORS
from models import Movies, Actors, setup_db, db
from sys import exc_info


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,-Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def check_healthy():
        return jsonify('Healthy')

    # get all movies
    @app.route('/movies', methods=['GET'])
    def show_movies():
        error = False
        try:
            movies = Movies.query.all()
            # parse data with format method
            formated = [movie.format() for movie in movies]

            return jsonify({
              "success": True,
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

    # get all actors
    @app.route('/actors', methods=['GET'])
    def show_actors():
        error = False
        try:
            actors = Actors.query.all()
            # parse data with format method
            formated = [actor.format() for actor in actors]

            return jsonify({
              "success": True,
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

    # add new movie
    @app.route("/movies", methods=['POST'])
    def add_movies():
        data = request.json
        try:
            # check full data in json object
            if data["title"] and data["release_date"]:
                title = data["title"]
                release_date = data["release_date"]

                movie = Movies(title=title, release_date=release_date)
                # insert data with insert method
                movie.insert()

                return jsonify({
                    "success": True,
                    "movie": movie.id
                })
            else:
                abort(422)
        except Exception:
            db.session.rollback()
            print(exc_info())
            abort(422)
        finally:
            db.session.close()

    # add new actor
    @app.route('/actors', methods=['POST'])
    def add_actors():
        data = request.json
        try:
            # check full data in json object
            if data["name"] and data["age"] and data["gender"]:
                name = data["name"]
                age = data["age"]
                gender = data["gender"]

                actor = Actors(name=name, age=age, gender=gender)
                # insert data with insert method
                actor.insert()
                return jsonify({
                    "success": True,
                    "actor": actor.id
                })
            else:
                abort(422)
        except Exception:
            db.session.rollback()
            print(exc_info())
            abort(422)
        finally:
            db.session.close()

    # delete movie with <id>
    @app.route("/movies/<movie_id>", methods=['DELETE'])
    def delete_movies(movie_id):
        try:
            movie = Movies.query.get(movie_id)
            if movie:
                # delete movie with delete method
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

    # delete actor with <id>
    @app.route("/actors/<actor_id>", methods=['DELETE'])
    def delete_actors(actor_id):
        try:
            actor = Actors.query.get(actor_id)
            if actor:
                # delete actor with delete method
                actor.delete()
                return jsonify({
                  "success": True,
                  "actor": actor.id
                })
            else:
                abort(404)
        except Exception:
            db.session.rollback()
            print(exc_info())
            abort(404)
        finally:
            db.session.close()

    # update existing movie with <id>
    @app.route("/movies/<movie_id>", methods=['PATCH'])
    def update_movies(movie_id):
        error = False
        data = request.json

        # get movie with spesific <id>

        title = data.get("title", None)
        release_date = data.get("release_date", None)
        try:
            movie = Movies.query.get(movie_id)
            if not movie:
                abort(404)
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            # update data with update method
            movie.update()

            return jsonify({
              "success": True,
              "movie": movie.format()
            })
        except Exception:
            db.session.rollback()
            print(exc_info())
            abort(404)
        finally:
            db.session.close()

    # update existing actor with <id>
    @app.route("/actors/<actor_id>", methods=['PATCH'])
    def update_actors(actor_id):
        error = False
        data = request.json

        # get actor with spesific <id>

        name = data.get("name", None)
        age = data.get("age", None)
        gender = data.get("gender", None)

        try:
            actor = Actors.query.get(actor_id)
            if not actor:
                abort(404)
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            # update data with update method
            actor.update()

            return jsonify({
              "success": True,
              "actor": actor.format()
            })
        except Exception:
            db.session.rollback()
            print(exc_info())
            abort(404)
        finally:
            db.session.close()

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Sorry, resource unavailable"
        }), 404

    @app.errorhandler(422)
    def unproccesable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Sorry, request cannot be processed"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "Sorry, Bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server error"
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)
