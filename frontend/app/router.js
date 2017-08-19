import Ember from 'ember';
import config from './config/environment';

const { Router } = Ember;

const router = Router.extend({
  location : config.locationType,
  rootURL  : config.rootURL
});

router.map(function() {
  this.route('sign-in');
  this.route('sign-out');
  this.route('user-home');
  this.route('sign-up');
  this.route('add-script');
  this.route('logout');
});

export default router;
