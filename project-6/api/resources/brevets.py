"""
Resource: Brevets
"""
from flask import Response, request, Flask
from flask_restful import Resource
import logging

# You need to implement this in database/models.py
from database.models import Brevet
from datetime import datetime

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

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


"""
GET http://API:PORT/api/brevets should display all brevets stored in the database.
GET http://API:PORT/api/brevet/ID should display brevet with id ID.
POST http://API:PORT/api/brevets should insert brevet object in request into the database.
DELETE http://API:PORT/api/brevet/ID should delete brevet with id ID.
PUT http://API:PORT/api/brevet/ID should update brevet with id ID with object in request.
"""

class BrevetsResource(Resource):
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        distance = input_json['distance']
        start_time = input_json['start_time']
        items = input_json['items']

        # (cannot parse date "2021-01-01T00:00": ['start_time'] 
        # open.cannot parse date "2021-01-01T01:28" 
        # close.cannot parse date "2021-01-01T03:30": ['items'])

        # https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')

        for item in items:
            item['open'] = datetime.strptime(item['open'], '%Y-%m-%dT%H:%M')
            item['close'] = datetime.strptime(item['close'], '%Y-%m-%dT%H:%M')
            
        result = Brevet(distance=distance, start_time=start_time, items=items).save()
        # result = Brevet(**input_json).save()
        return {'_id': str(result.id)}, 200
