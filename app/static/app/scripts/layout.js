console.log("layout.js")

app.controller('LayoutCtrl', [
  '$scope',
  '$rootScope',
  '$http',
  'Item',
  'Http',
  function($scope, $rootScope, $http, Item, Http){

    // Global functions
    // // Clear modal data
    $scope.init_modal = function(){
      $scope.modal = {
        index: undefined,
        type: undefined,
        post: {
          post_id: '',
          title: '',
          detail: '',
          zip_code: '',
          items: [],
          date_posted: "",
          time_posted: "",
        }
      }
    }
    $scope.hide_modal = function(selector){
      $(selector).modal('hide');
      // Clear the $scope.modal
      $scope.init_modal();
    }
    // // Prepare modal data for creating new post
    $scope.set_modal_create = function(){
      // First initialize
      $scope.init_modal();
      // Then set type
      $scope.modal.type = 'create';
      item = new Item({});
      console.log(item);
      item.owner_id = $scope.user_info.user_id;
      $scope.modal.post.items.push(item);
    }

    // // retrieve user_info from database
    $scope.get_user_info = function(){
      success_handler = function(data, status, headers, config){
        console.log(data);
        $scope.user_info = {
          'user_name': "",
          'user_id': '',
          'is_anonymous': true,
        }
        if ( !data.user_info.is_anonymous ){
          $scope.user_info.is_anonymous = false;
          $scope.user_info = {
            user_id : data.user_info.user_id,
            user_name : data.user_info.username
          }
        }
      }

      Http.request("GET", "/app/get_user/", {}, success_handler)
    }
    // // Submit data to the server
    $scope.create_post = function(){
      success_handler = function(data, status, header, config){
        $scope.hide_modal('#modal-create-post');
        $rootScope.$broadcast("new-post", data.new_post);
      }
      console.log('creating post');
      Http.request(
        'POST',
        'posts/',
        {
          post: $scope.modal.post,
          type: 'create',
        },
        success_handler
      )
    }

    // Initialize user_info and modal data
    $scope.init_modal();
    $scope.get_user_info();
}])