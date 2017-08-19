import Ember from 'ember';

const { run } = Ember;

export default function destroyApp(application) {
  run(application, 'destroy');
  if (window.server) {
    window.server.shutdown();
  }
}
