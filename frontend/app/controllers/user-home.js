// -*- coding: utf-8; mode: js; indent-tabs-mode: t; tab-width:2 -*-

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
  deleteScriptId:0,
  deleteScriptName:"",
  functionStringResults:"",
  codeResults:"",
  waitingForCode:false,
  runScriptFailed:false,

  reset() {
    clearTimeout(this.get("timeout"));
    this.setProperties({
      submitFailed: false,
      updateMessage: "updated successfully",
      updateDone: false,
      isProcessing: false,
      isSlowConnection: false,
      waitingForCode: false,
      runScriptFailed: false,
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

	//Editing your submitted scripts

  fetchedCodeSuccess(response) {
    this.reset();
    if (response.status==true){
      this.setProperties({
        updateMessage: "Retrieved from server",
        updateDone:true,
        clearTimer: setTimeout(this.clearUpdateMessage.bind(this), 1000),
        editorContents:response.Code,
        inputDescription:response.Code,
        inputTitle:response.Filename,
      });
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

	//Remote Execution of function strings
  showFunctionStringResults(response) {
    this.reset();
    this.set("functionStringResults",response.result);
		//TODO : check status key, and change highlight colour or something to indicate failure.
    Ember.$('#resultsModal').modal();
  },

	//Remote Execution of Scripts
  showFunctionResults(response) {
    this.reset();
    this.set("codeResults",response.result);
		//TODO : check status key, and change highlight colour or something to indicate failure.
    Ember.$('#runModal').modal();
  },
  runScriptError() {
    this.reset();
    this.set("runScriptFailed", true);
    this.set("failedMessage",'Submission failed. Server down? ');
  },
  runScriptFailure() {
    this.reset();
    this.set("runScriptFailed", true);
    this.set("failedMessage",'Submission failed. App Error. ');
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
    showDeleteDialog(script) {
      this.set("deleteScriptId",script.Id);
      this.set("deleteScriptName",script.Filename);
      Ember.$('#deleteModal').modal();
    },
    deleteScript(){
      Ember.$.post("/deleteScript", {"scriptId":this.deleteScriptId},this,'json');
      Ember.$('#deleteModal').modal('hide');
      this.send('refresh');
    },

		//Remote Execution of function strings
    executeFunctionString() {
      this.setProperties({
        isProcessing: true
      });
      var request = Ember.$.post("/evalFunctionString", {"function":this.functionString},this,'json');
      request.then(this.showFunctionStringResults.bind(this), this.runScriptFailure.bind(this), this.runScriptError.bind(this));
    },

		//Remote Execution of Scripts
    executeScript(script) {
      this.setProperties({
        waitingForCode: true,
        codeResults:"",
      });
      var request = Ember.$.post("/runScriptById", {'id':script.Id},this,'json');
      request.then(this.showFunctionResults.bind(this), this.failure.bind(this), this.error.bind(this));
    },



  },


});
