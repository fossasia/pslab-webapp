import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement () {
    Ember.$.jqplot(this.data.name,this.data.data,{
        title: this.title,
    });
  }
});
