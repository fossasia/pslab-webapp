<<<<<<< HEAD
[Heroku App](https://pslab-stage.herokuapp.com/)
=======

>>>>>>> 7958f6a4df9031fad841e78a6fbcbfc56e1028b1
# PSLab Remote Experiments

[![Build Status](https://travis-ci.org/fossasia/pslab-remote.svg?branch=master)](https://travis-ci.org/fossasia/pslab-remote)
[![Gitter](https://badges.gitter.im/fossasia/pslab.svg)](https://gitter.im/fossasia/pslab?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Deployment: [Heroku App](https://pslab-stage.herokuapp.com/)

## Introduction to the Virtual Lab

A virtual lab interface gives students remote access to equipment in laboratories via the internet without having to be physically present near the equipment.
The idea is that lab experiments can be made accessible to a larger audience which may not have the resources to set up the experiment at their place.
Another use-case scenario is that the experiment setup must be placed at a specific location which may not be habitable.

The PSLab’s capabilities can be increased significantly by setting up a framework that allows remote data acquisition and control.
It can then be deployed in various test and measurement scenarios such as an interactive environment monitoring station.

In the beginning, we will follow a basic [tutorial](https://code.tutsplus.com/series/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-827) to create a web-app using flask.

## Dependencies

### Backend

The virtual lab will be hosted using [Python-Flask](http://flask.pocoo.org/), which is a BSD Licensed microframework for Python based on Werkzeug and Jinja 2  .

It will use sqlalchemy to interface with databases containing user credentials and data. At present, postgresql will be used.

### Frontend

coming soon.

## Installing dependencies

+ Install sqlalchemy
  + sudo apt-get install python-sqlalchemy
  + provide the password. Username is root by default
+ install the Heroku CLI from [devcenter.heroku.com/articles/getting-started-with-python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)



The following command will install flask as well as dependencies such as Jinja2, itsdangerous, click, and Werkzeug

+ sudo pip install flask


## Running the app locally

`gunicorn app:app`
navigate to localhost:8000 in your web browser

## deploying to Heroku
+ [Staging](https://pslab-stage.herokuapp.com/)
+ production :



## Implemented features
- backend
  - [x] homepage hook
  - [x] SignUp hook
  - [ ] SignUp database updation procedure
  - [x] SignIn hook
  - [ ] SignIn database verification
  - [ ] User script page hook
  - [ ] Process and store a user written script

- Frontend
  - [x] css files : Bootstrap, custom css
  - [x] js files : Jquery
  - [x] homepage.html
  - [x] SignUp.html
  - [x] SignUp AJAX callbacks
  - [x] SignIn.html
  - [x] SignIn AJAX callback and redirection to user's homepage
  - [x] UserHome.html
  - [x] logout hook
  - [ ] Page to add a user written script


## Old resources
This project was moved from another repository, and in order to browse the various issues and PRs, the following links may help
+ [Initialize a virtual lab framework](https://github.com/fossasia/pslab-desktop-apps/pull/165)
+ [Sign-up process](https://github.com/fossasia/pslab-desktop-apps/pull/169)
+ [vlab sign-in process](https://github.com/fossasia/pslab-desktop-apps/pull/173)
