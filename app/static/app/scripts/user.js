console.log("user.js")

app.controller('UserCtrl', ['$scope', '$http', function($scope, $http){
  $scope.getArray = function(num) {
    array = [];
    i = 0;
    while (i < num){
      array[i] = i;
      i++;
    }
    return array
  }

  $http({
    method: 'POST',
    url: '',
  }).success(function(data, status, headers, config){
    console.log(data);
    $scope.posts = data;
  })
}])

.directive('userPostOverview', function(){
    return{
      restrict: "E",
      templateUrl: '/static/app/directives/user-post-overview.html',
    }
  })