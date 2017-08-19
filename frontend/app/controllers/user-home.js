import Ember from 'ember';

const { $, $: { post, extend }, Controller, get } = Ember;

export default Controller.extend({
  editTitle             : 'myFile',
/* ---- Add Script Screen ---*/
  inputDescription      : '',
  submitFailed          : false,
  failedMessage         : 'Failed to Login',
  updateDone            : false,
  updateMessage         : 'updated successfully',
  isProcessing          : false,
  isSlowConnection      : false,
  timeout               : null,
  clearTimer            : null,
  openCodeId            : null,
  fetchedCode           : null,
  editorContents        : '',
  deleteScriptId        : 0,
  deleteScriptName      : '',
  functionStringResults : '',
  codeResults           : '',
  waitingForCode        : false,
  runScriptFailed       : false,

  reset() {
    clearTimeout(this.get('timeout'));
    this.setProperties({
      submitFailed     : false,
      updateMessage    : 'updated successfully',
      updateDone       : false,
      isProcessing     : false,
      isSlowConnection : false,
      waitingForCode   : false,
      runScriptFailed  : false
    });
  },
  success(response) {
    this.reset();
    if (response.status) {
      this.setProperties({
        updateDone    : true,
        updateMessage : 'updated successfully',
        clearTimer    : setTimeout(this.clearUpdateMessage.bind(this), 1000)
      });
    }    else {
      this.set('submitFailed', true);
      this.failedMessage = String(response.message);
    }
  },

	// Editing your submitted scripts

  fetchedCodeSuccess(response) {
    this.reset();
    if (response.status) {
      this.setProperties({
        updateMessage    : 'Retrieved from server',
        updateDone       : true,
        clearTimer       : setTimeout(this.clearUpdateMessage.bind(this), 1000),
        editorContents   : response.Code,
        inputDescription : response.Code,
        inputTitle       : response.Filename
      });
    }    else {
      this.set('submitFailed', true);
      this.failedMessage = String(response.message);
    }
  },
  clearUpdateMessage() {
    this.set('updateDone', false);
  },
  error() {
    this.reset();
    this.set('submitFailed', true);
    this.set('failedMessage', 'Submission failed. Server down? ');
  },
  failure() {
    this.reset();
    this.set('submitFailed', true);
    this.set('failedMessage', 'Submission failed. App Error. ');
  },
  slowConnection() {
    this.set('isSlowConnection', true);
  },

	// Remote Execution of function strings
  showFunctionStringResults(response) {
    this.reset();
    this.set('functionStringResults', response.result);
		// TODO : check status key, and change highlight colour or something to indicate failure.
    $('#resultsModal').modal();
  },

	// Remote Execution of Scripts
  showFunctionResults(response) {
    this.reset();
    this.set('codeResults', response.result);
		// TODO : check status key, and change highlight colour or something to indicate failure.
    $('#runModal').modal();
  },
  runScriptError() {
    this.reset();
    this.set('runScriptFailed', true);
    this.set('failedMessage', 'Submission failed. Server down? ');
  },
  runScriptFailure() {
    this.reset();
    this.set('runScriptFailed', true);
    this.set('failedMessage', 'Submission failed. App Error. ');
  },


  actions: {
    openEditModal(script) {
      this.reset();
      this.openCodeId = script.Id;
      post('/getScriptById', { 'id': script.Id }, this, 'json')
        .then(this.fetchedCodeSuccess.bind(this), this.failure.bind(this), this.error.bind(this));
      $('#editModal').modal();
    },

    updateScript() {
      this.setProperties({
        submitFailed  : false,
        failedMessage : '',
        isProcessing  : true
      });
      this.set('timeout', setTimeout(this.slowConnection.bind(this), 1000));
      post('/updateCode', extend({}, this.getProperties('inputTitle', 'inputDescription'), { 'codeId': this.openCodeId }), this, 'json')
        .then(this.success.bind(this), this.failure.bind(this), this.error.bind(this));
    },
    showDeleteDialog(script) {
      this.set('deleteScriptId', script.Id);
      this.set('deleteScriptName', script.Filename);
      $('#deleteModal').modal();
    },
    deleteScript() {
      post('/deleteScript', { 'scriptId': this.deleteScriptId }, this, 'json');
      $('#deleteModal').modal('hide');
      this.send('refresh');
    },

    // Remote Execution of function strings
    executeFunctionString() {
      this.setProperties({
        isProcessing: true
      });
      post('/evalFunctionString', { 'function': this.functionString }, this, 'json')
        .then(this.showFunctionStringResults.bind(this), this.runScriptFailure.bind(this), this.runScriptError.bind(this));
    },
    // Remote Execution of Scripts
    executeScript(script) {
      this.setProperties({
        waitingForCode : true,
        codeResults    : ''
      });
      post('/runScriptById', { 'id': script.Id }, this, 'json')
        .then(this.showFunctionResults.bind(this), this.failure.bind(this), this.error.bind(this));
    },

    runButtonAction(actionDefinition) {
      if (actionDefinition.type === 'POST') {
        post('/evalFunctionString', { 'function': actionDefinition.endpoint }, this, 'json')
          .then(response => {
            const resultValue = get(response, actionDefinition.success.datapoint);
            if (actionDefinition.success.type === 'display_number') {
              $(`#${actionDefinition.success.target}`).text(resultValue.toFixed(3));
            } else if (actionDefinition.success.type === 'display') {
              $(`#${actionDefinition.success.target}`).text(resultValue);
            }
          });
      }
    }
  }
});
