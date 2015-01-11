console.log("this is login.js")

angular.module("continue")
.controller('LoginCtrl', [
  '$scope',
  '$http',
  function($scope, $http){

    // initialize all inputs
    $scope.user_name = "";
    $scope.password = "";
    $scope.signup_data = {
      "user_name": "",
      "email": "",
      "password": "",
      "password_confirm": "",
    }
    // Initialize other variables
    $scope.login_is_show = true;
    $scope.login_is_incomplete = false;
    $scope.signup_is_incomplete = false;
    $scope.success_msg = "";

    validate = function(method, input_data){
      is_valid = false;
      if (method == 'login'){
        // check if both fields are entered
        // If not, flash the inputs
        if ($scope.user_name.length * $scope.password.length == 0){
          console.log("incomplete");
          $scope.login_is_incomplete = true;
          setTimeout(
            function(){
              $scope.login_is_incomplete = false;
            },
            100
          );
        }
        else{
          is_valid = true;
        }
      }
      else if (method == 'signup'){
        ;
      }
      return is_valid;
    }

    $scope.login = function(){
      if ( validate('login') ){
        data = {
          'user_name': $scope.user_name,
          'password': $scope.password
        }
        $http({
          method: 'POST',
          url: '',
          data: data
        }).success(function(returned_data, status, headers, config){
          console.log(returned_data);
          if (returned_data.request_status == 'Logged in'){
            user_info = returned_data.user_info;
            $scope.user_info.user_name = user_info.user_name;
            $scope.user_info.user_id = user_info.user_id;
            $scope.user_info.is_anonymous = false;
            $scope.success_msg = "Welcome back " + user_info.user_name + ", you have successfully logged in!";
          }
          else if (returned_data.request_status == 'Invalid') {
            console.log("Invalid!!!");
            $scope.is_error = true;
          }
        });
      }
    }

    $scope.signup = function(){
      console.log("signup()");
      data = $scope.signup_data;
      console.log(data)
      // Check if all required fields are entered
      for (key in data) {
        if (data[key] == "" || data[key] == undefined){
          console.log(key);
          return;
        }
      }
      // If input are all entered, submit data
      console.log("begin signup");
      $http({
        method: "POST",
        url: '/app/signup/',
        data: data,
      }).success(function(data, status, headers, config){
        console.log(data);
        if (data.signup_is_success == true){
          console.log(data);
          user_info = data.user_info;
          $scope.user_info.user_name = user_info.user_name;
          $scope.user_info.user_id = user_info.user_id;
          $scope.user_info.is_anonymous = false;
          $scope.success_msg = "Welcome " + user_info.user_name + ", you have successfully signed up!";
        }
      })
    }
  }
])