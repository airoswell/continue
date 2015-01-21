// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("continue").controller("indexCtrl", [
    "$scope", function($scope) {
      $scope.tags_to_string = function(input_tags) {
        var areas, tag;
        if (input_tags) {
          areas = [
            (function() {
              var _i, _len, _results;
              _results = [];
              for (_i = 0, _len = input_tags.length; _i < _len; _i++) {
                tag = input_tags[_i];
                _results.push(tag.text);
              }
              return _results;
            })()
          ];
          areas = areas.join(",");
          return areas;
        }
        return "";
      };
      $("input[name='q']").on;
      $("input[name='q'], input[name='secret_key']").keyup(function(e) {
        if (e.which === 13) {
          return $scope.search();
        }
      });
      return $scope.search = function() {
        var areas, tags;
        areas = $scope.tags_to_string($scope.areas_tags);
        tags = $scope.tags_to_string($scope.tags_tags);
        $("input[name=areas]").val(areas);
        $("input[name=tags]").val(tags);
        document.getElementById('index-search-form').submit();
        return $("input").val("");
      };
    }
  ]);

}).call(this);
