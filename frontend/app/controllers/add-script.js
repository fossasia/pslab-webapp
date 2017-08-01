import Ember from 'ember';

export default Ember.Controller.extend({

/*---- Add Script Screen ---*/
  theme: 'ace/theme/cobalt',
  themes: [
    'ace/theme/cobalt',
    'ace/theme/ambiance',
    'ace/theme/chaos',
  ],
  inputDescription:"",
  submitFailed: false,
  failedMessage: "Failed to Login",
  isProcessing: false,
  isSlowConnection: false,
  timeout: null,

  success(response) {
    this.reset();
    if (response.status==true){
      this.reset();
      window.location.href = "/user-home";
    }
    else{
      this.set("submitFailed", true);
      this.failedMessage= String(response.message);
      }
  },
  error() {
    this.reset();
    this.set("submitFailed", true);
    this.set("failedMessage",'Submission failed. Server down? ');
  },
  failure() {
    this.reset();
    this.set("submitFailed", true);
    this.set("failedMessage",'Submission failed. App Error. ');
  },
  slowConnection() {
    this.set("isSlowConnection", true);
  },
  reset() {
    clearTimeout(this.get("timeout"));
    this.setProperties({
      isProcessing: false,
      isSlowConnection: false
      });
  },

  actions:{
    valueUpdated() {
      this.setProperties({
        submitFailed: false,
        failedMessage: "",
        isProcessing: true
      });
      this.set("timeout", setTimeout(this.slowConnection.bind(this), 1000));
      var request = Ember.$.post("/addScript", this.getProperties("inputTitle","inputDescription"),this,'json');
      request.then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
    },

  },
  
});
