/* eslint-env node */
'use strict';

const EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
  let app = new EmberApp(defaults, {
    // Add more options here
    ace: {
      themes  : ['cobalt', 'ambiance', 'chaos'],
      modes   : ['python', 'javascript'],
      workers : ['javascript']
    }
  });

  app.import('bower_components/bootstrap/dist/js/bootstrap.min.js');
  app.import('bower_components/bootstrap/dist/css/bootstrap.min.css');
  app.import('bower_components/bootstrap/dist/css/bootstrap.min.css.map');

  app.import('bower_components/bootstrap/dist/css/bootstrap-theme.min.css');
  app.import('bower_components/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2', {  destDir: 'fonts'  });


  app.import('bower_components/jqplot/jquery.jqplot.min.js');
  app.import('bower_components/jqplot/plugins/jqplot.cursor.js');
  app.import('bower_components/jqplot/plugins/jqplot.highlighter.js');
  app.import('bower_components/jqplot/plugins/jqplot.pointLabels.js');

  app.import('bower_components/jqplot/jquery.jqplot.min.css');
  return app.toTree([]);
};
