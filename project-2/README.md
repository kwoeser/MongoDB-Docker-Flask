Name: Karma Woeser
Project 2: Docker and flask
Due Date: Oct 16


# UOCIS322 - Project 2 #

This project will get you started with Docker and Flask. You need to have Docker set up on your machine to complete this project. You can alternatively use the machine we talked about in class.

## Getting started

* Go to `web/` and  read every line of the docker file and the flask app.

* Build the simple flask app image using

  ```
  docker build -t some-image-name .
  ```
  **Make sure to use a unique name if you're running on testium.**
* Run the container using

  ```
  docker run -d -p 5001:5000 some-image-name
  ```

* Launch `http://hostname:5001` using your web browser and check the output "UOCIS docker demo!".<br>
**Q:** What's `5001` and what's `5000`?<br>
**A:** the `-p` argument opens a container port to another on your local machine. Think of the container as its own separate machine, and assume you start a web server on port `5000` there. To access the web server from your machine, you forward container's `5000` to YOUR `5001`.<br>
To understand this better, try changing the `5001` when starting your container, or `5000`. But remember, `5000` should be the port Flask uses (see `web/app.py`).

## Tasks

The goal of this project is to implement a "file checking" logic, while also adding configuration reading to your Python script.

* If a file exists in `web/pages/` (i.e. `trivia.html`, any name, any extension or format) exists, transmit `200/OK` header followed by that file. 
    * Example: Running the service and binding its port to your machine's port 5000, and opening
      `http://localhost:5000/trivia.html` should display that page with a `200/OK` status code; similar to project-1.
* If the file doesn't exist, transmit an error code in the header along with the appropriate page html in the body. You'll do this by creating error handlers. You'll also create the following two html files with the error messages:
    * `web/pages/404.html` will display "File not found!"
    * `web/pages/403.html` will display "File is forbidden!"

    ⚠️ NOTE: if a request contains illegal characters (`..` or `~`), the response should be 403.

* Add a configuration parsing logic (like project 0) to `app.py` so that it looks for `credentials.ini`, and if not found `default.ini`, and reads the port number and debug mode from the file found.

* Update your email in `Dockerfile`. Update `README` with your name, info, and a brief description of the project.

* You will submit your credentials.ini in Canvas. It should include your name and repo URL.


## Grading Rubric

* If everything works as expected, 100 will be assigned.
* If existing pages and files are NOT handled correctly, 20 points will be docked.
* For each of the errors not handled correctly (403, and 404), 20 points will be docked.
* For each the two HTML files (`404.html` and `403.html`) not in the appropriate location, 5 points will be docked.
* If `README.md` is not updated with your name and info, 5 points will be docked.
* If `Dockerfile` doesn't contain your name and email, 5 points will be docked.
* If docker builds and runs, but does not have the expected functionalities implemented, or the server is unreachable, 20 will be assigned.
	* ⚠️ NOTE: If `app.py` does not read port number and debug mode from `credentials.ini` (or `default.ini` if not found), autograder will mark this as unreachable, as it cannot look for the correct port number.
* If docker builds, but fails to run, 15 will be assigned.
* If docker fails to build, 5 will be assigned.
* If `credentials.ini` is incorrect or not submitted, 0 will be assigned.

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
