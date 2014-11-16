console.log("This is compose.js")

app
  .controller('ComposeCtrl',
  [
    '$scope',
    '$http',
    'Item',
    'ItemSet',
    // 'ItemSet',
    function($scope, $http, Item, ItemSet){

      // initialization
      $scope.form_is_show = true;
      $scope.success_is_show = false;
      $scope.item_set = new ItemSet();
      $scope.items = $scope.item_set.items;
      $scope.post = {
        title: "",
        detail: "",
        zip_code: "",
        items: [],
      };  
      console.log(item_set);
      
      // ng-clicks
      $scope.add_item = function() {
        $scope.item_set.add_item();
      }

      $scope.set_cond = function(item, condition){
        item.condition = condition;
      }

      $scope.publish = function(){
        // Package user input
        data = {
          type: 'create',
          post: $scope.post,
        };
        data.post.items = $scope.items;
        $http({ 
          method: 'POST', 
          url: '/app/user/posts/',
          data: data
        }).success(function(data, status, headers, config){
          console.log(data);
          $scope.success_data = data;
          $scope.form_is_show = false;
          $scope.success_is_show = true;
        });
      };
  }])

  .directive('itemEditDetail', function(){
    return {
      restrict: 'E',
      templateUrl: '/static/app/directives/item-edit-detail.html',
    }
  })