# Distributed Computing Systems
## Distributed Square Matrix Multiplication
This program generates two **NxN** matrices filled with random integers from some range defined by user and returns result of their multiplication.

This is a project for college course on Wrocław University of Technology - it was not meant to be developed for practical usage in some bigger environment/system.

Please have in mention that this code can be optimized (and probably should), but it wasn't worth to care about it while developing. 
###Requirements
There are two conditions for this application to work that results from algorithm used:
* Number of computers/processes must be a *perfect square*
* Array dimension divided by square root of value from previous point must an integer.

##Algorithm
Algorithm based on [this presentation](http://www.cse.buffalo.edu/faculty/miller/Courses/CSE633/Ortega-Fall-2012-CSE633.pdf) by Patricia Ortega from University at Buffalo.

### Dependencies
Modules required for this projects:
* Numpy/Numpy.Matlib
* Pyro4

### Server.py
Server is 

Server requires two parameters during runtime:
* Host url
* Port

For the sake of this project I assume that we live in a happy world where data provided by server owner is always correct. It is more probable that person runnign this file on his server knows what he is doing. 

After initial setup program is running providing his functionality until stopped by user.

It is currently assumed that you run your application on port 9601, and then if you plan to run more than one instance on one server you use ports 9602, 9603... etc.

#### Safety
This project uses *pickle* to serialize objects. It is not too safe to use this serialization method, according to Pyro4 developers. Please refer to [this site](https://pythonhosted.org/Pyro4/security.html) for details.

### Client
Client program takes four arguments:
* Number or machines that we have available.
* Our matrices dimension.
* Range lower bound
* Range upper bound
At the end of runtime program shows result Array and how long program aws running.

Currently there is no plan for implementing reading host URLs from outside of program code. To add your own servers, please add them to array in line 81 of Client.py.
