import DS from 'ember-data';
import ENV from './config/environment';

export default DS.JSONAPIAdapter.extend({
  // Application specific overrides go here
  host: ENV.APP.API_HOST,
});

