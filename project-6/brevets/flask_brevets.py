"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
# import config
import requests

import logging
import os

# Import db functions from mongo.py
# from mongo import insert_items, fetch_items

###
# Globals
###
app = flask.Flask(__name__)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"



def api_get():
    """
    Obtains the newest document in the "lists" collection in database
    by calling the RESTful API.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    # Do we need to remove the / "GET /api//brevets HTTP/1.1". It doesn't seem to change anything.
    lists = requests.get(f"{API_URL}/brevets").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    items = lists[-1]
    return items["distance"], items["start_time"], items["items"]


def api_insert(distance, start_time, items):
    """
    Inserts a new to-do list into the database by calling the API.
    """
    _id = requests.post(f"{API_URL}/brevets", json={"distance": distance, "start_time": start_time, "items": items}).json()
    
    # Do we need to remove the / "GET /api//brevets HTTP/1.1". It doesn't seem to change anything.
    # _id = requests.post(f"{API_URL}brevets", json={"distance": distance, "start_time": start_time, "items": items}).json()
    return _id


from datetime import datetime
@app.route("/insert", methods=["POST"])
def insert():
    try: 
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!

        # Because input_json is a dictionary, we can do this:
        distance = input_json["distance"] 
        start_time = input_json["start_time"] 
        items = input_json["items"]


        # Change post request to make insert changes
        # start_time = datetime.fromisoformat(start_time)

        # for item in items:
        #     item["open"] = datetime.fromisoformat(input_json["open"])
        #     item["close"] = datetime.fromisoformat(input_json["close"])


        
        # MongoDB method
        # todo_id = insert_items(distance, start_time, items)   
        todo_id = api_insert(distance, start_time, items)

        return flask.jsonify(result={},
            message="Inserted!", 
            status=1, # This is defined by you. You just read this value in your javascript.
            mongo_id=todo_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/fetch")
def fetch():
        """
        /fetch : fetches the newest to-do list from the database.
        Accepts GET requests ONLY!
        JSON interface: gets JSON, responds with JSON
        """
        try:
            # MongoDB method
            # distance, start_time, items = fetch_items()
            distance, start_time, items = api_get()
            
            return flask.jsonify(
                result={"distance": distance, "start_time": start_time, "items":items}, 
                status=1,
                message="Successfully fetched!")
        except:
            return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch!")

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 0, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    # Grabs brevet start time and distance from JS
    brevet_start_time = request.args.get('start_time', 0, type = str) 

    # Arrow object
    # https://stackoverflow.com/questions/28087218/parse-date-and-time-from-string-with-time-zone-using-arrow
    start_time = arrow.get(brevet_start_time)
    

    brevet_dist = request.args.get('distance', 0, type = int)

    # if checkpoint is further than distance, set km to distance
    if km > brevet_dist:
        km = brevet_dist
        
    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    result = {
        "open": open_time, 
        "close": close_time
    }

    return flask.jsonify(result=result)

#############


app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
if __name__ == "__main__":
    # print("Opening for global access on port {}".format(port_num))
    app.run(port=port_num, host="0.0.0.0")
