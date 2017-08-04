import Ember from 'ember';

export default Ember.Route.extend({
beforeModel (){
    Ember.$.post("/logout", null,this);
    this.replaceWith('index')
  }

});
