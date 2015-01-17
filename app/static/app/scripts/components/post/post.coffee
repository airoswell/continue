angular.module "continue"

.controller "postCtrl", ["$scope", "Post", "ItemSelector", "ItemEditor", "Alert", ($scope, Post, ItemSelector, ItemEditor, Alert)->
  $scope.new_items = []
  $scope.post = Post.$build(Post.init)
  $scope.layout = {
    detail_input: false
  }

  # If 'id' is specified, load the post from server.
  $scope.$watch "id", ()->
    if $scope.id?
      $scope.post = Post.$find($scope.id)
      $scope.post.$then (response)->
        $scope.post.tags_handler()
        $('textarea').val($scope.post.detail).trigger('autosize.resize')
        if $scope.post.tags
          $scope.tags_input = [{"text": tag} for tag in $scope.post.tags][0]

  $scope.show_detail_editor = ()->
    $scope.layout.detail_input = true

  $scope.select_item = ()->
    Alert.show_msg("Loading your items ...")
    # $scope.post.items is passed in as existed items,
    # used to remove duplicated items from the BottomSheet.
    ItemSelector.begin($scope.post.items).then (response)->
      if response
        $scope.post.items.push(response)
        $scope.new_items.push(response)

  $scope.add_new_item = ()->
    ItemEditor.begin().then (response)->
      console.log "haha2 in add_new_item"
      if response
        $scope.post.items.push(response)
        $scope.new_items.push(response)

  $scope.save = ()->
    tags_array = [tag.text for tag in $scope.tags_input]
    tags = tags_array.join(",")
    $scope.post.tags = tags
    $scope.post.save().$then (response)->
      if "id" of response
        window.location.replace("/app/post/#{response.id}/")

]