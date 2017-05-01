Sumatra
=======
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![Coverage Status](https://coveralls.io/repos/github/cenkcorapci/sumatra/badge.svg?branch=master)](https://coveralls.io/github/cenkcorapci/sumatra?branch=master)
[![Build Status](https://travis-ci.org/cenkcorapci/sumatra.svg?branch=master)](https://travis-ci.org/cenkcorapci/sumatra)

A simple Reddit clone that uses a transient
 in-memory data storage.
 
 [Here is a demo](sumatra-app.herokuapp.com)
 
 > Pelease note that this app stores its data app context, which will make it probabilistic in 
 any load balanced/distributed environment such as Heroku and it will have data inconsistencies.  
### Features 
- Uses [Pykka](https://github.com/jodal/pykka) actor models for concurreny in in-memory data storage.
- Only supports one subreddit.
- Users can up vote and down vote and create new topics without authentication.Just enter your name for logging in.
### How to run
You have to be installed [pip](https://pypi.python.org/pypi/pip) for installing dependencies.After that, run
 ```
 pip install -r requirements.txt
 ```
 for installing dependencies.When you have installed dependencies you 
 boot up the app with following commands;
```
web: gunicorn -b 0.0.0.0:$PORT sumatra:app
```
or
```
python sumatra.py
```

### Tests
[Coverage](https://coverage.readthedocs.io/en/coverage-4.3.4/) is added to dependencies, so you
can run the unit tests by running the following command;
```
coverage run sumatra_spec.py
```
