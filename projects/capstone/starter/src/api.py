import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from jose import jwt

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES


# GET /drinks endpoint to show the list of drinks
@app.route("/drinks", methods=["GET"])
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    # print('drinks: ', drinks)
    formatted_drinks = [drink.short() for drink in drinks]
    # if formatted_drinks is None:
    #      abort(404)
    try:
        return jsonify({"success": True, "drinks": formatted_drinks})
    except Exception as e:
        print(e)
        abort(500)


# GET /drinks-detail endpoint to show the list of drinks details
@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_details(payload):
    drink_details = Drink.query.all()
    formatted_drink_details = [drink.long() for drink in drink_details]
    if formatted_drink_details is None:
        abort(404)
    try:
        return jsonify({"success": True, "drinks": formatted_drink_details})
    except Exception as e:
        print(e)
        abort(500)


# POST /drinks endpoint to create a new row in the drinks table
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def add_drinks(payload):
    body = request.get_json()
    if "title" not in body or "recipe" not in body:
        abort(400)
    try:
        req_recipe = body.get("recipe")
        new_title = body.get("title")
        new_recipe = json.dumps([req_recipe])
        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()

    except Exception as e:
        print(e)
        abort(404)

    return jsonify({"success": True, "drinks": [drink.long()]})


# PATCH /drinks/<id> endpoint to update an existing drink title
@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drinks(payload, id):
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


# DELETE /drinks/<id> endpoint to delete an existing drink
@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({"success": True, "id": id})
    except Exception as e:
        print(e)
        abort(500)


# Error Handling


# Error handlers
@app.errorhandler(401)
def not_found(error):
    return (
        jsonify({"success": False, "error": 401, "message": "Not authorized"}),
        401,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "Not found"}),
        404,
    )


@app.errorhandler(422)
def unprocessable_content(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Unprocessable Content"}),
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
        jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
        500,
    )


@app.errorhandler(AuthError)
def auth_error(e):
    return (
        jsonify({"success": False, "error": e.status_code, "message": e.error}),
        e.status_code,
    )
