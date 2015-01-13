
angular.module("continue")

.controller("DashBoardCtrl", [
  "$scope", "Post", "Item", "History", "Transaction"
  "Alert", "Auth", "Album", "BS"
  ($scope, Post, Item, History, Transaction, Alert, Auth, Album, BS) ->

    # Load in items and posts of the current user
    Alert.show_msg("Downloading your data.")
    $scope.items = Item.$search({items_per_page: 8}).$then ()->
      Alert.show_msg("Download is finished.")

    $scope.layout = {
      creating_new_item: false
      display_tab: "updates"
    }

    $scope.display_tab = (tab_name)->
      console.log "display_tab"
      $scope.layout.display_tab = tab_name

    $scope.scroll_to_post = (id)->
      top = $("#post-#{id}").offset().top
      $("html, body").animate scrollTop: top - 100
      true

    $scope.create_item = () ->
      if $scope.layout.creating_new_item
        return
      $scope.layout.creating_new_item = true
      $scope.layout.display_tab = "items"
      item = Item.$build(Item.init)
      item.is_new = true
      $scope.items.splice 0, 0, item
      $("html, body").animate scrollTop: $("#items-display").offset().top - 100
      true

    $scope.create_post = () ->
      if $scope.layout.creating_new_post
        return
      layout.creating_new_post = true
      post = Post.$build(Post.init)
      post.owner = Auth.get_user().user_id
      $scope.posts.splice 0, 0, post
      $("html, body").animate scrollTop: $("#posts-display").offset().top - 100
      true

    $scope.item_update_successHandler = (item, response) ->
      item.expanded = false
      item.new_status = ""

    $scope.item_create_successHandler = (item, response) ->
      layout.creating_new_item = false
      item.expanded = false
      item.is_new = false
      item.new_status = ""
      $scope.histories.$refresh()

    $scope.post_create_successHandler = (item, response) ->
      layout.creating_new_post = false
      post.is_new = false

    $scope.post_update_successHandler = (item, response) ->
      console.log "successfully updated the post."

    $scope.add_item = (post)->
      post.add_item()

    $scope.add_existing_item = (post)->
      item = post.add_item()
      BottomSheet.show(item)
])


