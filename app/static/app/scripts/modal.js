console.log("modal.js");

app.controller('ModalCtrl', ['$scope', 'Item', function($scope, Item){
  console.log('ModalCtrl');

  $scope.set_cond = function(item, condition){
    item.condition = condition;
  }

  $scope.add_item = function() {
    item = new Item({});
    item.owner_id = $scope.user_info.user_id;
    $scope.modal.post.items.push(item);
  }

  $scope.remove_item = function(index) {
    if ($scope.modal.post.items.length == 1){
      console.log("You need to have at least one item.");
      return;
    }
    console.log("remove_item");
    $scope.modal.post.items.splice(index, 1);
  }
}])