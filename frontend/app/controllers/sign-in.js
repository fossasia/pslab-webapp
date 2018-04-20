import Ember from 'ember';

const { $: { post }, Controller } = Ember;

export default Controller.extend({

/* ---- Login Screen ---*/

  loginFailed        : false,
  loginFailedMessage : 'Failed to Login',
  isProcessing       : false,
  isSlowConnection   : false,
  timeout            : null,

  success(response) {
    this.reset();
    if (response.status) {
      this.reset();
      this.transitionToRoute('user-home');
    }    else {
      this.set('loginFailed', true);
      this.loginFailedMessage = String(response.message);
    }
  },
  error() {
    this.reset();
    this.set('loginFailed', true);
    this.set('loginFailedMessage', 'Sign-In failed. Server down? ');
  },
  failure() {
    this.reset();
    this.set('loginFailed', true);
    this.set('loginFailedMessage', 'Sign-In failed. App Error. ');
  },
  slowConnection() {
    this.set('isSlowConnection', true);
  },
  reset() {
    clearTimeout(this.get('timeout'));
    this.setProperties({
      isProcessing     : false,
      isSlowConnection : false
    });
  },

  actions: {

    logMeIn() {
      this.setProperties({
        loginFailed        : false,
        loginFailedMessage : '',
        isProcessing       : true
      });

      this.set('timeout', setTimeout(this.slowConnection.bind(this), 1000));
      post('/validateLogin', this.getProperties('inputEmail', 'inputPassword'), this, 'json')
        .then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
    },

    togglePassword(checked) {     // To toggle the password visibility in login form
      this.set('any', checked);
      if (checked === true) {
        document.getElementById('inputPassword').type = 'text';
      } else {
        document.getElementById('inputPassword').type = 'password';
      }
    }

  }

});

