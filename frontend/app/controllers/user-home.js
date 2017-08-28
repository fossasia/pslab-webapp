import Ember from 'ember';
import { zip } from 'lodash';

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
  sourceCode            : '',
  waitingForCode        : false,
  runScriptFailed       : false,
  viewModalTitle        : '',
  viewContents          : '',
  viewAceInit(editor) {
    editor.setHighlightActiveLine(false);
    editor.setShowPrintMargin(false);
    editor.getSession().setTabSize(2);
    editor.getSession().setMode('ace/mode/python');
    editor.setReadOnly(true);
  },

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
    this.set('sourceCode', response.Code);
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
    openViewModal(script) {
      $('#viewModal').modal();
      post('/getScriptByFilename', { 'Filename': script.Filename }, this, 'json')
        .then(response => {
          if (response.status) {
            this.setProperties({
              viewContents   : response.Code,
              viewModalTitle : response.Filename
            });
          } else {
            this.set('viewModalTitle', 'Could not retrieve script!');
          }
        });
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
    executeScript(script, mode) {
      this.setProperties({
        waitingForCode : true,
        codeResults    : ''
      });
      if (mode === 'Id') {
        post('/runScriptById', { 'Id': script.Id }, this, 'json')
          .then(this.showFunctionResults.bind(this), this.failure.bind(this), this.error.bind(this));
      } else if (mode === 'Filename') {
        post('/runScriptByFilename', { 'Filename': script.Filename }, this, 'json')
          .then(this.showFunctionResults.bind(this), this.failure.bind(this), this.error.bind(this));
      }
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
            } else if (actionDefinition.success.type === 'update-plot') {
              if (actionDefinition.success.stacking === 'xy') {
                // alert(JSON.stringify($(`#${actionDefinition.success.target}`).data(), null, 4));
                // $(`#${actionDefinition.success.target}`).data('jqplot').replot({ data: [zip(null, resultValue)] });
                $.jqplot(actionDefinition.success.target, [zip(...resultValue)]).replot();
              } else if (actionDefinition.success.stacking === 'xyy') {
                $.jqplot(actionDefinition.success.target, [zip(...[resultValue[0], resultValue[1]]), zip(...[resultValue[0], resultValue[2]])]).replot();
              } else if (actionDefinition.success.stacking === 'xyyyy') {
                $.jqplot(actionDefinition.success.target, [zip(...[resultValue[0], resultValue[1]]), zip(...[resultValue[0], resultValue[2]]), zip(...[resultValue[0], resultValue[3]]), zip(...[resultValue[0], resultValue[4]])]).replot();
              } else {
                $.jqplot(actionDefinition.success.target, resultValue).replot();
              }
            }
          });
      }
    }
  }
});
