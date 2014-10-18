console.log("This is index.js");

app = angular.module('PassOn', []);

app
  .controller('TestCtrl', ['$scope', function($scope){
    $scope.variable = "some var."
  }])

  .directive('itemDetail', function(){
    return {
      restrict: 'E',
      templateUrl: '/static/app/directives/item-detail.html',
    }
  })