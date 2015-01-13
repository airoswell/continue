// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("continue.auth", ["restmod"]).factory("Auth", [
    "restmod", function(restmod) {
      var User, user;
      User = restmod.model("/users/");
      user = {};
      return {
        get_user_profile: function() {
          return User.$search().$asPromise();
        },
        store_user: function(response) {
          return user = response;
        },
        get_user: function() {
          return user;
        }
      };
    }
  ]);

}).call(this);
