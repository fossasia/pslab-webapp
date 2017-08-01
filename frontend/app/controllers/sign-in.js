import Ember from 'ember';

export default Ember.Controller.extend({

/*---- Login Screen ---*/

  loginFailed: false,
  loginFailedMessage: "Failed to Login",
  isProcessing: false,
  isSlowConnection: false,
  timeout: null,

    success: function(response) {
         this.reset();
         if (response.status==true){
                this.reset();
                window.location.href = "/userHome";
         }
         else{
                this.set("loginFailed", true);
                this.loginFailedMessage= String(response.message);
         }
    },
    error: function() {
         this.reset();
         this.set("loginFailed", true);
         this.set("loginFailedMessage",'Sign-In failed. Server down? ');
    },
    failure: function() {
         this.reset();
         this.set("loginFailed", true);
         this.set("loginFailedMessage",'Sign-In failed. ? ');
    },

    slowConnection: function() {
         this.set("isSlowConnection", true);
    },

    reset: function() {
         clearTimeout(this.get("timeout"));
         this.setProperties({
              isProcessing: false,
              isSlowConnection: false
         });
    },



  actions:{

      logMeIn: function() {
        this.setProperties({
         loginFailed: false,
         loginFailedMessage: "",
         isProcessing: true
        });

        this.set("timeout", setTimeout(this.slowConnection.bind(this), 100));
        var request = Ember.$.post("/validateLogin", this.getProperties("inputEmail", "inputPassword"),this,'json');
        request.then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
      },


  },
  
});


