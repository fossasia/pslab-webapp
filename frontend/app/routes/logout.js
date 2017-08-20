import Ember from 'ember';

const { Route, $: { post } } = Ember;

export default Route.extend({
  beforeModel() {
    post('/logout', null, this);
    this.replaceWith('index');
  }

});
