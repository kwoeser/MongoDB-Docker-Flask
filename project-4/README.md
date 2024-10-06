# UOCIS322 - Project 4 #
You'll learn how to write test cases and test your code, along with more JQuery.

## Overview

You will reimplement RUSA ACP controle time calculator with Flask and AJAX.
> That's *"controle"* with an *e*, because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.

### ACP controle times

This project consists of a web application that is based on RUSA's online calculator. The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data. 

## Tasks

* Implement the logic in `acp_times.py` based on the algorithm linked above.

* Create test cases using the original website, and write test suites for your project.
	* Based on what was discussed in the lecture, create test cases, try them in the original website, and check if your functions correctly calculate the times.
	* This will effectively replicate the calulator above.

* Edit the template and Flask app so that the required remaining arugments are passed along.
	* Currently the miles to kilometers (and some other basic stuff) is implemented with AJAX. 
	* The remainder is left to you.

* As always, revise the README file, and add your info to `Dockerfile`. These have points!
	* **NOTE:** This time, you should outline the application, the algorithm, and how to use start (docker instructions, web app instructions). **Make sure you're thorough, otherwise you may not get all the points.**

* As always, submit your `credentials.ini` through Canvas. It should contain your name and git repo URL.

### Testing

A suite of nose test cases is a requirement of this project. Design the test cases based on an interpretation of rules here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Be sure to test your test cases: You can use the current brevet time calculator [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html) to check that your expected test outputs are correct. While checking these values once is a manual operation, re-running your test cases should be automated in the usual manner as a Nose test suite.

To make automated testing more practical, your open and close time calculations should be in a separate module. Because I want to be able to use my test suite as well as yours, I will require that module be named `acp_times.py` and contain the two functions I have included in the skeleton code (though revised, of course, to return correct results).

We should be able to run your test suite by changing to the `brevets` directory and typing `nosetests`. All tests should pass. You should have at least 5 test cases, and more importantly, your test cases should be chosen to distinguish between an implementation that correctly interprets the ACP rules and one that does not.

## Grading Rubric

* If your code works as expected: 100 points. This includes:

	* Completing the frontend in `calc.html`.
	
	* Completing the Flask app accordingly (`flask_brevets.py`).
	
	* Implementing the logic in `acp_times.py`.
	
	* Updating `README` with a clear specification.
	
	* Writing at least **five** correct tests using nose (put them in `tests`, follow Project 3 if necessary) and all pass.

* If the algorithm is incorrect, 25 points will be docked off.

* If the webpage does not work as expected (JQuery or Flask failing to correctly fill in the information, etc.), 25 points will be docked off.

* If the test cases are missing/not functional/do not all pass, 5 points will be docked off per each (25 points total).

* If `README` is not clear, missing or not edited, or `Dockerfile` is not updated, up to 15 points will be docked off.

* If none of the functionalities work, 10 points will be given assuming `credentials.ini` is submitted with the correct repo URL, and `Dockerfile` builds and runs without any errors. 

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
