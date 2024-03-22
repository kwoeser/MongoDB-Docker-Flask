"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.


"""
GET http://API:PORT/api/brevets should display all brevets stored in the database.
GET http://API:PORT/api/brevet/ID should display brevet with id ID.
POST http://API:PORT/api/brevets should insert brevet object in request into the database.
DELETE http://API:PORT/api/brevet/ID should delete brevet with id ID.
PUT http://API:PORT/api/brevet/ID should update brevet with id ID with object in request.
"""

class BrevetResource(Resource):
    # Taken from TodolistRESTful app and changed
    def get(self, id):
        brevet = Brevet.objects.get(id=id).to_json()
        return Response(brevet, mimetype="application/json", status=200)

    def put(self, id):
        input_json = request.json
        Brevet.objects.get(id=id).update(**input_json)
        return '', 200

    def delete(self, id):
        Brevet.objects.get(id=id).delete()
        return '', 200