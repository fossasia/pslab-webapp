[Heroku App](https://pslab-stage.herokuapp.com/)

# PSLab Remote Experiments

[![Build Status](https://travis-ci.org/fossasia/pslab-remote.svg?branch=master)](https://travis-ci.org/fossasia/pslab-remote)
[![Gitter](https://badges.gitter.im/fossasia/pslab.svg)](https://gitter.im/fossasia/pslab?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[Backend API server](https://pslab-stage.herokuapp.com/) : Hosted on Heroku. The dyno is reaped after an hour of inactivity and may take up to 10 seconds to boot up.
[Webapp](https://pslab-remote.surge.sh) : Hosted on surge.sh

## Introduction to the Virtual Lab

A virtual lab interface gives students remote access to equipment in laboratories via the internet without having to be physically present near the equipment.
The idea is that lab experiments can be made accessible to a larger audience which may not have the resources to set up the experiment at their place.
Another use-case scenario is that the experiment setup must be placed at a specific location which may not be habitable.

The PSLab’s capabilities can be increased significantly by setting up a framework that allows remote data acquisition and control.
It can then be deployed in various test and measurement scenarios such as an interactive environment monitoring station.

## Introductory blog posts

+ [Designing a remote access framework with PSLab](http://blog.fossasia.org/designing-a-virtual-laboratory-with-pslab/)
+ [Creating backend API methods suing Python Flask](http://blog.fossasia.org/designing-a-remote-laboratory-with-pslab-using-python-flask-framework/)
+ [Execute python function calls remotely](http://blog.fossasia.org/designing-a-remote-laboratory-with-pslab-execution-of-function-strings/)
+ [Deploying the API server and Webapp to separate domains automaticaly ](http://blog.fossasia.org/pslab-remote-lab-automatically-deploying-the-emberjs-webapp-and-flask-api-server-to-different-domains/)
+ [Creating better structured apps from user submitted scripts](http://blog.fossasia.org/enhancing-the-functionality-of-user-submitted-scripts-in-the-pslab-remote-framework/)
+ [Adding a graph component to the frontend](http://blog.fossasia.org/including-a-graph-component-in-the-remote-access-framework-for-pslab/)

## Structure

### Backend

The virtual lab will be hosted using [Python-Flask](http://flask.pocoo.org/), which is a BSD Licensed microframework for Python based on Werkzeug and Jinja 2  .
It will use sqlalchemy to interface with databases containing user credentials and data. At present, postgresql will be used.

The repository has been integrated with Heroku, and modifications to the master branch are automatically deployed to pslab-stage.herokuapp.com after the CI build passes

### Frontend

The frontend code resides in a subdirectory called `frontend` . It is Designed with EmberJS , and a production build is automatically deployed to pslab-remote.surge.sh by the CI if the build is successful.

## Installing dependencies

+ Install all packages in requirements.txt
+ navigate to the frontend directory, and run `npm install`


## Running the app locally

`gunicorn app:app`
This launches the API server on default port 8000

`cd frontend`
`ember -s environment='development'`
this launches the the emberjs webapp on port 4200

navigate to localhost:4200 in your web browser


## Implemented features
- backend
  - [x] homepage hook
  - [x] SignUp hook
  - [x] SignUp database updation procedure
  - [x] SignIn hook
  - [x] SignIn database verification
  - [x] User script page hook
  - [x] Store, Edit, View, Delete user submitted code snippets
  - [x] Execute a function string
  - [x] Execute a code snippet
  - [x] Create object oriented apps

- New Frontend based on EmberJS
  - [x] Home Page
  - [x] Navbar with bootstrap styling
  - [x] sign-up page
  - [x] sign-in page
  - [x] user-home.html. Feature to Create and Store code snippets. Execute function strings
  - [x] Create/Edit/Delete/Execute Python scripts. Embedded ace-js code editor.
  - [x] Display object oriented applications
  - [x] Plot data with the integrated JQplot library

## Old resources
This project was moved from another repository, and in order to browse the various issues and PRs, the following links may help
+ [Initialize a virtual lab framework](https://github.com/fossasia/pslab-desktop-apps/pull/165)
+ [Sign-up process](https://github.com/fossasia/pslab-desktop-apps/pull/169)
+ [vlab sign-in process](https://github.com/fossasia/pslab-desktop-apps/pull/173)
