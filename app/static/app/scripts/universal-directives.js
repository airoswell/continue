// Generated by CoffeeScript 1.8.0
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  angular.module("continue").filter("requested", function() {
    return function(user_id, item) {
      var requester, requesters_id;
      requesters_id = [
        (function() {
          var _i, _len, _ref, _results;
          _ref = item.requesters;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            requester = _ref[_i];
            _results.push(requester.id);
          }
          return _results;
        })()
      ];
      if (__indexOf.call(requesters_id, user_id) >= 0) {
        return true;
      }
      return false;
    };
  }).filter("previously_owned", function() {
    return function(user_id, item) {
      return __indexOf.call(item.previous_owners, user_id) >= 0;
    };
  }).directive("autoExpand", function() {
    "<div auto-expand data=\"<the input variable>\" init-width=\"100px\"\n    min-size=\"20\">\n    ...\n    <input tyle='text' ng-model=\"<the input variable>\">\n</div>";
    return {
      restrict: "AE",
      scope: {
        data: "=",
        minSize: "@",
        initWidth: "@"
      },
      link: function(scope, element, attrs) {
        var auto_expand, input;
        if (scope.minSize === void 0) {
          scope.minSize = 7;
        }
        if (scope.initWidth === void 0) {
          scope.initWidth = "80px";
        }
        auto_expand = function(data) {
          var size;
          size = Math.floor(data.toString().length / 5) * 5 + 6;
          if (size > scope.minSize) {
            input.attr({
              "size": size
            });
            return input.css({
              "width": "auto"
            });
          }
        };
        input = element.find("input");
        return scope.$watch("data", function() {
          if (input.length === 0) {
            input = element.find("input");
          }
          if (!scope.data) {
            input.css({
              "width": scope.initWidth
            });
          }
          if (scope.data) {
            return auto_expand(scope.data);
          }
        });
      }
    };
  }).directive("clickToShow", function() {
    " template\n<div click-to-show>\n  <div click-to-show-trigger></div>\n  <div click-to-show-target></div>\n</div>\nclicking the '[click-to-show-trigger]' will show and hide\n'[click-to-show-trigger]'.";
    return {
      restrict: "A",
      scope: true,
      link: function(scope, element, attrs) {
        var target, trigger;
        scope.expanded = false;
        trigger = element.find("[click-to-show-trigger]");
        target = element.find("[click-to-show-target]");
        target.css({
          "display": "none"
        });
        return trigger.on("click", function(e) {
          if (!scope.expanded) {
            target.css({
              "display": ""
            });
          } else if (scope.expanded) {
            target.css({
              "display": "none"
            });
          }
          scope.expanded = !scope.expanded;
          return scope.$apply();
        });
      }
    };
  }).directive("angularItemEditMenu", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/item-edit-menu.html",
      link: function(scope, element, attrs) {
        scope.refresh = false;
        if (__indexOf.call(attrs, "refresh") >= 0) {
          return scope.refresh = attrs["refresh"];
        }
      }
    };
  }).directive("itemEditButton", [
    "ItemEditor", "$rootScope", function(ItemEditor, $rootScope) {
      return {
        restrict: "A",
        link: function(scope, element, attrs) {
          var item_id, refresh;
          if ("itemId" in attrs) {
            item_id = attrs['itemId'];
          }
          refresh = false;
          if ("refresh" in attrs) {
            refresh = attrs['refresh'];
          }
          return scope.show_editor = function() {
            var promise;
            if (item_id) {
              promise = ItemEditor.begin(item_id, refresh);
            } else {
              scope.item.is_new = false;
              promise = ItemEditor.begin(scope.item, refresh);
            }
            return promise.then(function(response) {
              var existing_items, i, _i, _ref;
              if (scope.view === "post") {
                console.log("We are in view post!!!");
                existing_items = scope.post.items;
                console.log("scope.post.items", scope.post.items);
                for (i = _i = 0, _ref = existing_items.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
                  console.log("existing_items[" + i + "]", existing_items[i]);
                  if (existing_items[i].id === response.id) {
                    existing_items[i] = response;
                  }
                }
                return console.log("After the update, scope.post.items = ", scope.post.items);
              }
            });
          };
        }
      };
    }
  ]).directive("dropDownMenu", [
    "$timeout", function($timeout) {
      return {
        restrict: "A",
        scope: true,
        link: function(scope, element, attrs) {
          var target, trigger;
          trigger = element.find("[drop-down-menu-trigger]");
          target = element.find("[drop-down-menu-target]");
          target.css({
            "position": "absolute",
            "display": "none"
          });
          trigger.on("click", function(e) {
            target.css({
              "display": ""
            });
            return console.log("clicked!");
          });
          return $("html").click(function(a) {
            if (!$.contains(element[0], a.target)) {
              return target.css({
                "display": "none"
              });
            }
          });
        }
      };
    }
  ]).directive("postItemDeleteButton", [
    "Item", function(Item) {
      return {
        restrict: "A",
        scope: true,
        link: function(scope, element, attrs) {
          var item_id, post_id;
          item_id = attrs["itemId"];
          post_id = attrs["postId"];
          scope.show_double_check = false;
          scope.double_check = function() {
            console.log("double_check scope", scope);
            return scope.show_double_check = true;
          };
          return scope.del = function() {
            var item;
            console.log("del");
            console.log("del scope", scope);
            scope.show_double_check = false;
            return item = Item.$find(item_id).$then(function(response) {
              item.remove_from_post = post_id;
              return item.save();
            });
          };
        }
      };
    }
  ]).directive("itemTitle", function() {
    return {
      restrct: "E",
      scope: {
        item: "="
      },
      templateUrl: "/static/app/directives/item-title.html",
      link: function(scope, element, attrs) {
        return console.log("itemTitle");
      }
    };
  }).directive("angularItemOverviewHeader", function() {
    return {
      restrct: "E",
      templateUrl: "/static/app/directives/angular-item-overview-header.html"
    };
  }).directive("angularItemOverview", function() {
    return {
      restrict: "E",
      templateUrl: "/static/app/directives/angular-item-overview.html"
    };
  });

}).call(this);
