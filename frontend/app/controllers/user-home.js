import Ember from 'ember';

export default Ember.Controller.extend({
editTitle:"myFile",
/*---- Add Script Screen ---*/
  inputDescription:"",
  submitFailed: false,
  failedMessage: "Failed to Login",
  updateDone: false,
  updateMessage: "updated successfully",
  isProcessing: false,
  isSlowConnection: false,
  timeout: null,
  clearTimer: null,
  openCodeId:null,
  fetchedCode:null,
  editorContents:"",

  reset() {
    clearTimeout(this.get("timeout"));
    this.setProperties({
      submitFailed: false,
      updateDone: false,
      isProcessing: false,
      isSlowConnection: false
      });
  },
  success(response) {
    this.reset();
    if (response.status==true){
      this.setProperties({
        updateDone:true,
        updateMessage: "updated successfully",
        clearTimer:setTimeout(this.clearUpdateMessage.bind(this), 1000)
        });
    }
    else{
      this.set("submitFailed", true);
      this.failedMessage= String(response.message);
      }
  },
  fetchedCodeSuccess(response) {
    this.reset();
    if (response.status==true){
      this.set("updateDone",true);
      this.set("clearTimer", setTimeout(this.clearUpdateMessage.bind(this), 1000));
      this.set("editorContents",response.Code);
      this.set("inputDescription",response.Code);
      this.set("inputTitle",response.Filename);
    }
    else{
      this.set("submitFailed", true);
      this.failedMessage= String(response.message);
      }
  },
  clearUpdateMessage(){
    this.set("updateDone",false);
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

  actions:{
    openEditModal(script) {
      this.reset();
      this.openCodeId = script.Id;
      var request = Ember.$.post("/getScriptById", {'id':script.Id},this,'json');
      request.then(this.fetchedCodeSuccess.bind(this), this.failure.bind(this), this.error.bind(this));
      Ember.$('#editModal').modal();
    },
    updateScript() {
      this.setProperties({
        submitFailed: false,
        failedMessage: "",
        isProcessing: true
      });
      this.set("timeout", setTimeout(this.slowConnection.bind(this), 1000));
      var request = Ember.$.post("/updateCode", Ember.$.extend({},this.getProperties("inputTitle","inputDescription"),{"codeId":this.openCodeId}),this,'json');
      request.then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
    },

  },



});
