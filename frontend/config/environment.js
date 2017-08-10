/* eslint-env node */
'use strict';

module.exports = function(environment) {
  let ENV = {
    modulePrefix: 'pslab-frontend',
    environment,
    rootURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
	    API_HOST: 'http://127.0.0.1:8000',
    }
  };


switch (environment) {
	case 'development':
		ENV.APP.usingCors = true;
		ENV.APP.corsWithCreds = true;
		ENV.APP.apiURL = 'http://localhost:8000'
		break;
	// make alias in /etc/hosts 127.0.0.1   localhost mybackend.com
	case 'cors-hack':
		ENV.APP.usingCors = true;
		ENV.APP.corsWithCreds = true;
		ENV.APP.apiURL = 'http://mybackend.com:8000'
		break;
	case 'production':
		ENV.APP.usingCors = true;
		ENV.APP.corsWithCreds = true;
		ENV.APP.apiURL = 'https://pslab-stage.herokuapp.com'
		break;
	case 'test':
		ENV.locationType = 'none';

		// keep test console output quieter
		ENV.APP.LOG_ACTIVE_GENERATION = false;
		ENV.APP.LOG_VIEW_LOOKUPS = false;

		ENV.APP.rootElement = '#ember-testing';
		break;
}


  return ENV;
};
