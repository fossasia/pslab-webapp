import Ember from 'ember';

export function initJqplot(element) {

  var plot1 = Ember.$.jqplot(element.name,element.data,{
      title: 'My New Plot',
  });
  return "done";
}

export default Ember.Helper.helper(initJqplot);
