angular.module "continue"

.controller "postCtrl", [
  "$scope", "Post", "ItemSelector", "ItemEditor", "Alert", "$http"
  ($scope, Post, ItemSelector, ItemEditor, Alert, $http)->
    $scope.new_items = []
    $scope.post = Post.$build(Post.init)
    $scope.layout = {
      detail_input: false
    }
    $scope.submission_error = false
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


    $scope.reset = ()->
      console.log "reseting."
      $scope.post.$fetch()
      $scope.new_items = []

    $scope.save = ()->
      if not $scope.postEditor.$valid
        $scope.submission_error = true
        Alert.show_error("You input maybe incomplete, or invalid.")
        return
      if $scope.post.visibility == "Invitation" and not $scope.post.secret_key
        $scope.missing_key = true
      tags_array = [tag.text for tag in $scope.tags_input]
      tags = tags_array.join(",")
      $scope.post.tags = tags
      $scope.post.save().$then (response)->
        if "id" of response
          window.location.replace("/app/post/#{response.id}/")
      , (e)->
        console.log e

]