// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("worldsheet").directive("dashboardHistoryOverview", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/dashboard-history-overview.html",
      link: function(scope, element, attrs) {}
    };
  }).directive("dashboardItemOverview", [
    "History", "Album", "Alert", function(History, Album, Alert) {
      return {
        restrict: "E",
        templateUrl: "/static/app/directives/dashboard-item-overview.html",
        link: function(scope, element, attrs) {
          scope.expand = function(item) {
            console.log("item.expanded isnt true", item.expanded !== true);
            if (item.expanded !== true) {
              console.log("expand");
              item.expanded = true;
              item.histories = item.histories.$search({
                items_per_page: 8
              });
            } else {
              console.log("fold");
              item.expanded = false;
              item.histories = History;
            }
          };
          scope.get_albums = function(item) {
            Alert.show_msg("Downloading your albums ...");
            return Album.get_albums().then(function(response) {
              return item.pic = response;
            });
          };
          return element.on("click", function(e) {
            if ("trigger" in e.target.attributes) {
              scope.expand(scope.item);
              return scope.$apply();
            }
          });
        }
      };
    }
  ]).directive("inputText", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/input-text.html",
      scope: {
        data: "=",
        label: "=",
        placeHolder: "=",
        inputClass: "=",
        containerClass: "="
      }
    };
  }).directive("inputDropdown", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/input-dropdown.html",
      scope: {
        data: "=",
        label: "=",
        choices: "=",
        containerClass: "=",
        transfer: "=",
        user: "="
      },
      link: function(scope, element, attrs) {
        scope.dropdown = false;
        element.find("[trigger]").on("click", function() {
          scope.dropdown = true;
          return scope.$apply();
        }).on("mouseleave", function() {
          scope.dropdown = false;
          return scope.$apply();
        });
        return scope.select = function(option) {
          return scope.data = option;
        };
      }
    };
  }).directive("inputTextarea", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/input-textfield.html",
      scope: {
        data: "=",
        label: "=",
        containerClass: "@",
        inputClass: "@",
        placeHolder: "="
      }
    };
  }).directive("inputDate", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/input-date.html",
      scope: {
        date: "=",
        label: "@"
      }
    };
  }).directive("inputNum", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/input-num.html",
      scope: {
        num: "=",
        label: "@"
      },
      link: function(scope, element) {
        return scope.click = function() {
          element.find("input").focus();
          return true;
        };
      }
    };
  }).directive("contenteditable", function() {
    return {
      restrict: "A",
      require: "ngModel",
      link: function(scope, element, attrs, ngModel) {
        var read;
        read = function() {
          ngModel.$setViewValue(element.html());
        };
        ngModel.$render = function() {
          element.html(ngModel.$viewValue || "");
        };
        element.bind("blur keyup change", function() {
          scope.$apply(read);
        });
      }
    };
  });

}).call(this);
