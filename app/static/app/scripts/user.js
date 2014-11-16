console.log("user.js")

app.controller('UserCtrl', ['$scope', '$http', 'Http', 'Item', function($scope, $http, Http, Item){
  $scope.getArray = function(num) {
    array = [];
    i = 0;
    while (i < num){
      array[i] = i;
      i++;
    }
    return array
  }
  // Retrieve all posts by the user
  $scope.get_posts = function(){
    $http({
      method: 'POST',
      url: 'posts/',
      data: {
        type: 'get',
      }
    }).success(function(data, status, headers, config){
      console.log(data);
      $scope.posts = data.reverse();
    })
  }


  $scope.set_modal_edit = function(post, index){
    $scope.modal['index'] = index;
    $scope.modal['type'] = 'edit';
    // Set the post in modal to be the same as current post
    $scope.modal.post = post;
    console.log(post)
    // post is the current post
  }

  $scope.update_post = function(){
    success_handler = function(data, status, headers, config){
      if( data.success ){
        index = $scope.modal.index;
        $scope.posts[index] = data.post;
        $('#modal-edit-post').modal('hide');
        // Clear the $scope.modal
        $scope.init_modal();
      }
      else{
        console.log("There is some server error!");
      }
    }
    console.log("update_post");
    Http.request(
      'POST',
      'posts/',
      {
        post: $scope.modal.post,
        type: 'edit',
      },
      success_handler
    );
  }

  $scope.delete_post = function(){
    console.log("delete!");
    Http.request(
      'POST',
      'posts/',
      {
        post: $scope.modal.post,
        type: 'delete',
      },
      function(data, status, headers, config){
        console.log("data", data);
        if (data.success){
          console.log("Finally deleted!")
          $scope.posts.splice($scope.modal['index'], 1);
          $scope.hide_modal('#modal-edit-post');
        }
      }
    )
  }

  $scope.$on('new-post', function(event, post){
    $scope.posts.splice(0, 0, post)
  });

  // Initialize user's posts
  $scope.get_posts();
}])

.directive('userPostOverview', function(){
    return{
      restrict: "E",
      templateUrl: '/static/app/directives/user-post-overview.html',
    }
  })