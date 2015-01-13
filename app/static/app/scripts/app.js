// Generated by CoffeeScript 1.8.0
(function() {
  var app;

  app = angular.module("continue", ["ngResource", "ngAria", "ngAnimate", "ngMaterial", "restmod", "continue.auth", "continue.models", "continue.social_accounts", "ngTagsInput"]);

  app.config([
    "$httpProvider", function($httpProvider) {
      $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
      $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
      $httpProvider.defaults.xsrfCookieName = "csrftoken";
      return $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    }
  ]);

}).call(this);
