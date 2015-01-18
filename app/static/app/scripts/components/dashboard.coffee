
angular.module("continue")

.controller("DashBoardCtrl", [
  "$scope", "Post", "Item", "Feed", "Timeline", "Alert", "Auth",
  ($scope, Post, Item, Feed, Timeline, Alert, Auth) ->

    # Load in items and posts of the current user
    Alert.show_msg("Downloading your data.")
    $scope.items = Item.$search({num_of_records: 8}).$then ()->
      this.tags_handler()
      Alert.show_msg("Download is finished.")

    $scope.layout = {
      creating_new_item: false
      display_tab: "items"
      loading:
        "posts": false
        "feeds": false
        "timeline": false
        "items": false
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
        $scope.posts.tags_handler()
      .$asPromise().then ()->
        $scope.layout.loading.posts = false
      , ()->
        Alert.show_msg("You have reach the end of the posts.")

    $scope.load_items = ()->
      $scope.layout.loading.items = true
      if not $scope.items
        $scope.items = Item.search({"start": 0})
      else
        $scope.items = $scope.items.fetch({"start": $scope.items.start})

      $scope.items.$then (response)->
        self = this
        # store the next [start] param; it will propagate to
        # queryset[start:end]
        if self.start == 0
          self.start = parseInt($scope.numOfPosts) + self.length
        else
          self.start = parseInt($scope.numOfPosts) + self.length
        # Deal with the tags
        # initialize the tags_input and tags_private_input
        # Now convert the tags from <string> to <array>
        this.tags_handler()
      .$asPromise().then ()->
        $scope.layout.loading.items = false
      , ()->
        Alert.show_msg("You have reach the end of the posts.")

    $scope.load_feeds = ()->
      $scope.layout.loading.feeds = true
      if not $scope.feeds
        $scope.feeds = Feed.$search(
          # $scope.feed_starts are the initial starts passed from views.py
          {"starts": $scope.feed_starts}
        )
      else
        $scope.feeds = $scope.feeds.$fetch(
          {"starts": $scope.feeds.starts}
        )

      $scope.feeds.$then (response)->
        $scope.feeds.starts = $scope.feed_starts
        # Begin processing the returned data
        for feed in $scope.feeds
          # Process the post.tags
          if feed.model_name == "Post"
            $scope.feeds.starts.Post += 1
            post = feed
            if post.tags
              if typeof(post.tags) == "string"
                post.tags = post.tags.split(",")
            else
              post.tags = []
          if feed.model_name == "Item"
            $scope.feeds.starts.Item += 1
            item = feed
            if item.tags
              if typeof(item.tags) == "string"
                item.tags = item.tags.split(",")
            else
              item.tags = []
          else if feed.model_name == "ItemEditRecord"
            $scope.feeds.starts.ItemEditRecord += 1
      .$asPromise().then ()->
        $scope.layout.loading.feeds = false
      , ()->
        Alert.show_msg("All feeds are already loaded.")


    $scope.load_timeline = ()->
      $scope.layout.loading.timeline = true
      # Download data
      if not $scope.timeline
        $scope.timeline = Timeline.$search(
          # $scope.feed_starts are the initial starts passed from views.py
          {"starts": $scope.timeline_starts}
        )
      else
        $scope.timeline = $scope.timeline.$fetch(
          {"starts": $scope.timeline.starts}
        )

      $scope.timeline.$then (response)->
        $scope.timeline.starts = {}
        for model_name of $scope.timeline_starts
          $scope.timeline.starts[model_name] = $scope.timeline_starts[model_name]
        # Begin processing the returned data
        for feed in $scope.timeline
          # Process the post.tags
          if feed.model_name == "ItemTransactionRecord"
            $scope.timeline.starts.ItemTransactionRecord += 1
          else if feed.model_name == 'ItemEditRecord'
            $scope.timeline.starts.ItemEditRecord += 1
      .$asPromise().then ()->
        $scope.layout.loading.timeline = false
      , ()->
        Alert.show_msg("All timeline records are downloaded.")

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


