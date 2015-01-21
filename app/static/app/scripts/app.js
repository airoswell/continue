// Generated by CoffeeScript 1.8.0
(function() {
  var app;

  app = angular.module("continue", ["ngResource", "ngAria", "ngAnimate", "ngMaterial", "restmod", "ui.bootstrap.typeahead", "ui.bootstrap.tooltip", "continue.auth", "continue.models", "continue.social_accounts", "ngTagsInput", "infinite-scroll", "hc.marked", "omr.angularFileDnD"]);

  app.config([
    "$httpProvider", function($httpProvider) {
      $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
      $httpProvider.defaults.xsrfCookieName = "csrftoken";
      return $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    }
  ]);

  app.config([
    'markedProvider', function(markedProvider) {
      return markedProvider.setOptions({
        gfm: true
      });
    }
  ]);

  app.factory("settings", function() {
    var STATIC_URL, UPLOADED_URL;
    STATIC_URL = "http://104.237.144.150/static/";
    UPLOADED_URL = "" + STATIC_URL + "uploaded/";
    return {
      STATIC_URL: STATIC_URL,
      UPLOADED_URL: UPLOADED_URL
    };
  });

  angular.module("template/tooltip/tooltip-popup.html", []).run([
    "$templateCache", function($templateCache) {
      return $templateCache.put("template/tooltip/tooltip-popup.html", "<div class=\"tooltip {{placement}}\" ng-class=\"{ in: isOpen(), fade: animation() }\">\n" + "  <div class=\"tooltip-arrow\"></div>\n" + "  <div class=\"tooltip-inner\" ng-bind=\"content\"></div>\n" + "</div>\n" + "");
    }
  ]);

}).call(this);
