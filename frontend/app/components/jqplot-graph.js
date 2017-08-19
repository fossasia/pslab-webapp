import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement () {
    Ember.$.jqplot(this.data.name,this.data.data,{
        title: this.title,

        axes: {
          xaxis: {
            tickInterval: 1,
            rendererOptions: {
            minorTicks: 4
            }
          },
        },
        highlighter: {
          show: true, 
          showLabel: true, 

          tooltipAxes: 'xy',
          sizeAdjust: 9.5 , tooltipLocation : 'ne'
        },				  
        legend: {
          show: true,
          location: 'e',
          rendererOptions: {
            numberColumns: 1,
          }
        },
        cursor:{ 
          show: true,
          zoom:true, 
          showTooltip:false
          } 

    });
  }
});
