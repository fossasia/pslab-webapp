import Ember from 'ember';

export default Ember.Route.extend({
model(){
  return Ember.$.getJSON('/getScriptList'); //[{"Date": "Sat, 29 Jul 2017 18:08:46 GMT", "Filename": "asd", "Id": 1}];
},
actions: {
  refresh: function() {
    this.refresh();
  }
},
});
