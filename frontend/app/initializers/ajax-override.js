/* global jQuery */
import ENV from '../config/environment';

export function initialize(/* application */) {
  if (ENV.APP.usingCors) {
    (function($) {
      const _old = $.ajax;
      $.ajax = function() {
        let url, settings, { APP: { apiURL } } = ENV;

				/* Handle the different function signatures available for $.ajax() */
        if (arguments.length === 2) {
          url = arguments[0];
          settings = arguments[1];
        } else {
          settings = arguments[0];
        }

        settings.crossDomain = true;
        if (!settings.xhrFields) {
          settings.xhrFields = {};
        }
        settings.xhrFields.withCredentials = true;

        if (!url) {
          url = settings.url;
        }

				/* If we still don't have an URL, execute the request and let jQuery handle it */
        if (!url) {
          return _old.apply(this, [settings]);
        }

				/* combine the apiURL and the url request if necessary */
        if (!url.includes(apiURL)) {
					/* Do we need a '/'? */
          if (url[0] !== '/' && apiURL[apiURL.length - 1] !== '/') {
            url = `/${  url}`;
          }
          url = apiURL + url;
        }
        settings.url = url;

        return _old.apply(this, [settings]);
      };
    })(jQuery);
  }
}

export default {
  name: 'ajax-override',
  initialize
};
