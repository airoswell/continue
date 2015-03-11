// Generated by CoffeeScript 1.8.0
(function() {
  var app;

  app = angular.module("worldsheet", ["ngResource", "ngAria", "ngAnimate", "ngMaterial", "restmod", "ui.bootstrap", "worldsheet.models", "worldsheet.social_accounts", "ngTagsInput", "infinite-scroll", "hc.marked", "angularFileUpload", 'angular-jqcloud']);

  app.config([
    "$httpProvider", function($httpProvider) {
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
    var HOST_URL, STATIC_URL, UPLOADED_URL;
    console.log("settings factory");
    if (LIVEHOST === "True") {
      HOST_URL = "http://104.237.144.150";
    } else if (LIVEHOST === "False") {
      HOST_URL = "http://localhost:8000";
    }
    console.log("LIVEHOST = ", LIVEHOST);
    STATIC_URL = "" + HOST_URL + "/static";
    UPLOADED_URL = "" + STATIC_URL + "/uploaded/";
    return {
      STATIC_URL: STATIC_URL,
      UPLOADED_URL: UPLOADED_URL
    };
  });

}).call(this);
