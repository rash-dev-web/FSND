import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

#   Endpoints:
# GET /actors and /movies
# DELETE /actors/ and /movies/
# POST /actors and /movies and
# PATCH /actors/ and /movies/
  
  @app.route("/")
  def welcome_page():
      return "Casting Agency Home Page"


  # GET endpoint to get the list of actors
  @app.route("/actors", methods=["GET"])
  def get_drinks():
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [actor.short() for actor in actors]
      try:
          return jsonify({"success": True, "actors": formatted_actors})
      except Exception as e:
          print(e)
          abort(500)

  
  # GET endpoint to get the list of movies
  @app.route("/movies", methods=["GET"])
  def get_movies():
      movies = Movie.query.order_by(Movie.id).all()
      formatted_movies = [movie.short() for movie in movies]
      try:
          return jsonify({"success": True, "movies": formatted_movies})
      except Exception as e:
          print(e)
          abort(500)
  
  # DELETE enpoint to delete an actor from db
  @app.route("/actors/<int:id>", methods=["DELETE"])
  # @requires_auth("delete:actors")
  def delete_actors(payload, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
        return jsonify({"success": True, "id": id})
    except Exception as e:
        print(e)
        abort(500)

  # DELETE enpoint to delete a movie from db
  @app.route("/movies/<int:id>", methods=["DELETE"])
  # @requires_auth("delete:movies")
  def delete_movies(payload, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({"success": True, "id": id})
    except Exception as e:
        print(e)
        abort(500)

  # POST endpoint to add an actor to db
  @app.route("/actors", methods=["POST"])
  # @requires_auth("post:actors")
  def add_actor(payload):
    body = request.get_json()
    if "name" not in body or "age" not in body or "gender" not in body:
        abort(400)
    try:
        new_name = body.get("name")
        new_age = body.get("age")
        new_gender = body.get("gender")
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()

    except Exception as e:
        print(e)
        abort(404)

    return jsonify({"success": True, "actors": [actor.long()]})
  
  # POST endpoint to add a movie to db
  @app.route("/movies", methods=["POST"])
  # @requires_auth("post:movies")
  def add_movies(payload):
    body = request.get_json()
    if "title" not in body or "release_date" not in body:
        abort(400)
    try:
        new_title = body.get("title")
        new_release_date = body.get("release_date")
        movie = Movie(title=new_title, release_date=new_release_date)
        movie.insert()

    except Exception as e:
        print(e)
        abort(404)

  # PATCH endpoint to update an actor
  @app.route("/actors/<int:id>", methods=["PATCH"])
  # @requires_auth("patch:actors")
  def patch_actors(payload, id):
    body = request.get_json()
    if "title" not in body:
        abort(400)
    try:
        updated_title = body.get("title")
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.title = updated_title
        drink.update()

    except Exception as e:
        print(e)
        abort(404)

    return jsonify({"success": True, "drinks": [drink.long()]})
  # PATCH endpoint to update a movie

  # Error handlers
  @app.errorhandler(404)
  def not_found(error):
       return (
            jsonify({"success": False, "error": 404, "message": "Not found"}),
            404,
        )

  @app.errorhandler(422)
  def unprocessable_content(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable Content"}
            ),
            422,
        )

  @app.errorhandler(400)
  def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad Request"}),
            400,
        )

  @app.errorhandler(500)
  def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal Server Error"}
            ),
            500,
        )

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)