import Ember from 'ember';

const { Route, $: { getJSON } } = Ember;

export default Route.extend({
  model() {
    return getJSON('/getScriptList'); // [{"Date": "Sat, 29 Jul 2017 18:08:46 GMT", "Filename": "asd", "Id": 1}];
  },
  actions: {
    refresh() {
      this.refresh();
    }
  }
});
