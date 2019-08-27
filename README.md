# PSLab Webapp

This repository holds the code for the PSLab Webapp to enable students to access the [Pocket Science Lab (PSLab)](https://pslab.io) open hardware platform and other equipment through the Internet.

[![Build Status](https://travis-ci.org/fossasia/pslab-webapp.svg?branch=master)](https://travis-ci.org/fossasia/pslab-webapp)
[![Mailing List](https://img.shields.io/badge/Mailing%20List-FOSSASIA-blue.svg)](https://groups.google.com/forum/#!forum/pslab-fossasia)
[![Gitter](https://badges.gitter.im/fossasia/pslab.svg)](https://gitter.im/fossasia/pslab?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Twitter Follow](https://img.shields.io/twitter/follow/pslabio.svg?style=social&label=Follow&maxAge=2592000?style=flat-square)](https://twitter.com/pslabio)

The goal of the PSLab Webapp is to create a virtual lab that can give students remote access to Pocket Science Labs and other equipment in laboratories via the internet without having to be physically present near the equipment. PSLab is a tiny pocket science lab that provides an array of equipment for doing science and engineering experiments. It can function like an oscilloscope, waveform generator, frequency counter, programmable voltage and current source and also as a data logger. Our website is at https://pslab.io

## Buy

* You can get a Pocket Science Lab device from the [FOSSASIA Shop](https://fossasia.com).
* More resellers are listed on the [PSLab website](https://pslab.io/shop/).

## Communication

* The PSLab [chat channel is on Gitter](https://gitter.im/fossasia/pslab).
* Please also join us on the [PSLab Mailing List](https://groups.google.com/forum/#!forum/pslab-fossasia).

## Development Goals of PSLab Webapp Virtual Lab

A virtual lab interface can give students remote access to equipment in laboratories via the internet without having to be physically present near the equipment. The idea is that lab experiments can be made accessible to a larger audience which may not have the resources to set up the experiment at their place. Another use-case scenario is that the experiment setup must be placed at a specific location which may not be habitable. The capabilities of the Pocket Science Lab can be increased significantly by setting up a framework that allows remote data acquisition and control. It can then be deployed in various test and measurement scenarios such as an interactive environment monitoring station.

## Deployments
* [Backend API server](https://pslab-stage.herokuapp.com/) is hosted on Heroku. The dyno is reaped after an hour of inactivity and may take up to 10 seconds to boot up.
* [Webapp Frontend ](https://pslab-remote.surge.sh) is hosted on surge.sh

## Introductory blog posts

+ [Designing a remote access framework with PSLab](http://blog.fossasia.org/designing-a-virtual-laboratory-with-pslab/)
+ [Creating backend API methods using Python Flask Framework](http://blog.fossasia.org/designing-a-remote-laboratory-with-pslab-using-python-flask-framework/)
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

Setting up PSLab is really easy. The steps are:
1. Ensure you have the following dependencies to setup PSLab:
- Python3/2
- Git
- Nodejs
2. Clone the pslab-webapp repositary via git.
```shell
 git clone https://github.com/fossasia/pslab-webapp.git && cd pslab-webapp/
```
3. Install all Python packages in requirements.txt
```
pip install -r requirements.txt
```
4. Install the frontend dependcies as well
```
cd frontend/
npm install
```

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
