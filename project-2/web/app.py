"""
John Doe's Flask API.
"""

from flask import Flask, send_from_directory
import os
import configparser

app = Flask(__name__)

@app.route("/<string:name>")
@app.errorhandler(403)
@app.errorhandler(404)
def hello(name):
    try:
        if ".." in name or "~" in name:
            return forbidden()
        else:
            return send_from_directory('pages/', name), 200
    
    except:
        return not_found()


@app.route("/")
def index():
    return "UOCIS docker demo!\n"

# Forbidden error 
def forbidden():
    return send_from_directory('pages/', '403.html'), 403

# Not Found error
def not_found():
    return send_from_directory('pages/', '404.html'), 404

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
#message = config["SERVER"]
port = config["SERVER"]["PORT"]
debug = config["SERVER"]["DEBUG"]


if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port = port)
