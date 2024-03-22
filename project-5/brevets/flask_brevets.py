"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
import os

# Import db functions from mongo.py
from mongo import insert_items, fetch_items

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

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

        todo_id = insert_items(distance, start_time, items)

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
            distance, start_time, items = fetch_items()
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

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
