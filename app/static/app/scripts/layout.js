console.log("layout.js")

app.controller('LayoutCtrl', ['$scope', '$http', function($scope, $http){
  $scope.user_info = {
    is_anonymous: true,
    user_id: "",
    user_name: "",
  }

  // On load, fetch current user data, and make it available
  // to the entire scope.
  $http({
    method: "GET",
    url: "/app/get_user/",
  }).success(function(data, status, headers, config){
    $scope.user_info = {
      'user_name': "",
      'user_id': '',
      'is_anonymous': true,
    }
    console.log(data);
    if ( !data.user_info.is_anonymous ){
      $scope.user_info.is_anonymous = false;
      $scope.user_info = {
        user_id : data.user_info.user_id,
        user_name : data.user_info.username
      }
    }
  })
}])