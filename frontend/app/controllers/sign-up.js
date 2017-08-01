import Ember from 'ember';

export default Ember.Controller.extend({

/*---- Sign Up Controller ---*/

  signUpFailed: false,
  failedMessage: "Failed to Sign Up",
  isProcessing: false,
  isSlowConnection: false,
  timeout: null,

  success(response) {
    this.reset();
    if (response.status==true){
      this.reset();
      window.location.href = "/";
    }
    else{
      this.set("signUpFailed", true);
      this.failedMessage= String(response.message);
      }
  },
  error() {
    this.reset();
    this.set("signUpFailed", true);
    this.set("failedMessage",'Sign-Up failed. Server down? ');
  },
  failure() {
    this.reset();
    this.set("signUpFailed", true);
    this.set("failedMessage",'Sign-Up failed. ? ');
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

    signMeUp() {
      this.setProperties({
        signUpFailed: false,
        failedMessage: "",
        isProcessing: true
      });

      this.set("timeout", setTimeout(this.slowConnection.bind(this), 100));
      var request = Ember.$.post("/signUp", this.getProperties("inputName","inputEmail","inputPassword"),this,'json');
      request.then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
    },

  },
  
});

/*
 
    <script type="text/javascript">
       $(function() {
		$('#btnSignUp').click(function() {
	 
			$.ajax({
				url: '/signUp',
				data: $('form').serialize(),
				type: 'POST',
				dataType:'json',
				success: function(response) {
					if (response.hasOwnProperty('error')){
						$('#message').css("color", "red");
						$('#message').html(String(response.error));
						}
					else if (response.hasOwnProperty('message')){
						$('#message').css("color", "green");
						$('#message').html(response.message);
						}
					console.log(response);
				},
				error: function(response) {
					$('#message').css("color", "red");
					$('#message').html('Sign-Up failed. ');
					console.log(response);
				}
			});
		});
	});

	</script>

*/
