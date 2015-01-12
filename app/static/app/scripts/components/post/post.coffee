angular.module "continue"

.controller "postCtrl", ["$scope", "Post", "ItemSelector", "ItemEditor", ($scope, Post, ItemSelector, ItemEditor)->
  $scope.new_items = []
  $scope.post = Post.$build(Post.init)
  # If 'id' is specified, load the post from server.
  $scope.$watch "id", ()->
    if $scope.id?
      $scope.post = Post.$find($scope.id)
      $scope.post.$then (response)->
        console.log $scope.post = response

  $scope.select_item = ()->
    ItemSelector.begin($scope.post.items).then (response)->
      if response
        $scope.post.items.push(response)
        $scope.new_items.push(response)

  $scope.add_new_item = ()->
    ItemEditor.begin().then (response)->
      if response
        $scope.post.items.push(response)
        $scope.new_items.push(response)

  $scope.save = ()->
    console.log "In postCtrl $scope.post.owner", $scope.post.owner
    $scope.post.save().$then (response)->
    #   # window.location.replace("/app/post/#{response.id}/");

]