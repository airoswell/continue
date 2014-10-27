console.log("This is results.js")

app
  .controller('SearchResultsCtrl',
  [
    '$scope',
    '$http',
    function($scope, $http, Item, ItemSet){
      // Process data passed from Django via ng-init
      $scope.$watch('search_string', function(){
        console.log("search_loc = ", $scope.search_loc)
        console.log("search_string = ", $scope.search_string)
        data = {
          'search_string': $scope.search_string,
          'search_loc': $scope.search_loc
        }
        $http({ 
          method: 'GET', 
          url: 'process/?search_string=iPad&search_loc=11790',
          // data: data,
        }).success(function(data, status, headers, config){
          console.log(data);
          $scope.posts = data;
        });
      });

      $scope.modal = {
        post:{
          title: "",
          detail: "",
          owner: "",
          zip_code: "",
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

      condition_generator = function(condition){
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

      $scope.setModal = function(post){
        modal = $scope.modal;
        modal.post = {
          title: post.title,
          detail: post.detail,
          owner: post.owner,
          zip_code: post.zip_code,
          items: [],
        }
        for (i=0; i<post.items.length; i++){
          item = post.items[i];
          current_item = {
            title: item.title,
            quantity: item.quantity,
            condition: condition_generator(item.condition),
            detail: item.detail,
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