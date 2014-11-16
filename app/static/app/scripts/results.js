
console.log("This is results.js")

app
  .controller('SearchResultsCtrl',
  [
    '$scope',
    '$http',
    function($scope, $http, Item, ItemSet){
      // Process data passed from Django via ng-init
      $scope.$watch('search_string', function(){
        data = {
          'search_string': $scope.search_string,
          'search_loc': $scope.search_loc
        }
        $http({ 
          method: 'GET', 
          url: 'process/?search_string=' + $scope.search_string + '&search_loc=' + $scope.search_loc,
        })
        .success(function(data, status, headers, config){
          console.log(data);
          $scope.posts = data;
        });
      });
      // Initialize variables for modal
      $scope.modal_result = {
        post:{
          id: undefined,
          title: "",
          detail: "",
          owner: "",
          zip_code: "",
          date_posted: "",
          time_posted: "",
          items: [],
        }
      }

      $scope.getArray = function(num) {
        array = [];
        i = 0;
        while (i < num){
          array[i] = i;
          i++;
        }
        return array
      }

      condition_writer = function(condition){
        if (condition == 'Nw'){
          return 'New';
        }
        else if (condition == 'Ln'){
          return "Like new";
        }
        else if (condition == 'Gd'){
          return 'Good';
        }
        else{
          return 'Functional';
        }
      }

      status_writer = function(status){
        if (status == 'av'){
          return 'Available';
        }
        else if (status == 'po'){
          return 'Passed on';
        }
        else if (status == 'dp'){
          return 'Disposed';
        }
        else if (status == 'dl'){
          return 'Deleted';
        }
      }

      $scope.set_modal_result = function(post){
        modal = $scope.modal_result;
        modal.post = {
          id: post.id,
          title: post.title,
          detail: post.detail,
          owner: post.owner,
          zip_code: post.zip_code,
          items: [],
          date_posted: post.date_posted,
          time_posted: post.time_posted,
        }
        for (i=0; i<post.items.length; i++){
          item = post.items[i];
          current_item = {
            id: item.id,
            title: item.title,
            quantity: item.quantity,
            condition: condition_writer(item.condition),
            detail: item.detail,
            status: status_writer(item.status),
          };
          modal.post.items.push(current_item);
        }
      }
  }])

  .directive('postOverview', function(){
    return{
      restrict: "E",
      templateUrl: '/static/app/directives/post-overview.html',
    }
  })
  .directive('itemDetail', function(){
    return{
      restrict: "E",
      templateUrl: '/static/app/directives/item-detail.html',
    }
  })