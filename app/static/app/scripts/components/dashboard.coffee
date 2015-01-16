
angular.module("continue")

.controller("DashBoardCtrl", [
  "$scope", "Post", "Item", "Feed", "Alert", "Auth",
  ($scope, Post, Item, Feed, Alert, Auth) ->

    # Load in items and posts of the current user
    Alert.show_msg("Downloading your data.")
    $scope.items = Item.$search({num_of_records: 8}).$then ()->
      for item in $scope.items
        if item.tags
          item.tags_input = [{"text": tag} for tag in item.tags.split(",")][0]
      Alert.show_msg("Download is finished.")

    $scope.layout = {
      creating_new_item: false
      display_tab: "timeline"
      loading:
        "posts": false
        "feeds": false
        "timeline": false
    }

    $scope.load_posts = ()->
      $scope.layout.loading.posts = true
      if not $scope.posts
        $scope.posts = Post.search({"start": $scope.numOfPosts})
      else
        $scope.posts = $scope.posts.fetch({"start": $scope.posts.start})

      $scope.posts.$then (response)->
        # store the next [start] param; it will propagate to
        # queryset[start:end]
        if $scope.posts.start == 0
          $scope.posts.start = parseInt($scope.numOfPosts) + $scope.posts.length
        else
          $scope.posts.start = parseInt($scope.numOfPosts) + $scope.posts.length
        # Deal with the tags
        for post in $scope.posts
          if post.tags
            if typeof(post.tags) == "string"
              post.tags = post.tags.split(",")
          else
            post.tags = []
      .$asPromise().then ()->
        $scope.layout.loading.posts = false
      , ()->
        Alert.show_msg("You have reach the end of the posts.")

    $scope.load_feeds = ()->
      $scope.layout.loading.feeds = true
      if not $scope.feeds
        $scope.feeds = Feed.$search(
          # $scope.feed_starts are the initial starts passed from views.py
          {"feed_starts": $scope.feed_starts}
        )
      else
        $scope.feeds = $scope.feeds.$fetch(
          {"feed_starts": $scope.feeds.feed_starts}
        )

      $scope.feeds.$then (response)->
        console.log response
        feed_starts = response.pop()
        # Begin processing the returned data
        for feed in $scope.feeds
          # Process the post.tags
          if feed.model_name == "Post"
            post = feed
            if post.tags
              if typeof(post.tags) == "string"
                post.tags = post.tags.split(",")
            else
              post.tags = []
          if feed.model_name == "Item"
            item = feed
            if item.tags
              if typeof(item.tags) == "string"
                item.tags = item.tags.split(",")
            else
              item.tags = []


    $scope.load_timeline = ()->
      console.log "loading timeline"
      $scope.layout.loading.timeline = true
      if not $scope.timeline
        $scope.timeline = Feed.$search(
          # $scope.feed_starts are the initial starts passed from views.py
          {"timeline_starts": $scope.timeline_starts}
        )
      else
        $scope.timeline = $scope.timeline.$fetch(
          {"timeline_starts": $scope.timeline.timeline_starts}
        )

      $scope.timeline.$then (response)->
        console.log response
        timeline_starts = response.pop()
        # Begin processing the returned data
        for feed in $scope.timeline
          # Process the post.tags
          if feed.model_name == "Post"
            post = feed
            if post.tags
              if typeof(post.tags) == "string"
                post.tags = post.tags.split(",")
            else
              post.tags = []
          if feed.model_name == "Item"
            item = feed
            if item.tags
              if typeof(item.tags) == "string"
                item.tags = item.tags.split(",")
            else
              item.tags = []


    $scope.display_tab = (tab_name)->
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


