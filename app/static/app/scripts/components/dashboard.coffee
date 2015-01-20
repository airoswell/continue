
angular.module("continue")

.controller "DashBoardCtrl", [
  "$scope", "Post", "Item", "Feed", "Timeline", "Alert",
  "InfiniteScroll",
  ($scope, Post, Item, Feed, Timeline, Alert, InfiniteScroll) ->

    # Load in items and posts of the current user
    Alert.show_msg("Downloading your data.")
    $scope.items = Item.$search({num_of_records: 8}).$then ()->
      this.tags_handler()
      Alert.show_msg("Download is finished.")

    $scope.layout = {
      creating_new_item: false
      display_tab: "posts"
      show_items_search_results: false
      loading:
        "posts": false
        "feeds": false
        "timeline": false
        "items": false
    }

    $scope.items_search = (tag)->
      Alert.show_msg("Searching...")
      $scope.layout.items_search_keyword = tag
      $scope.layout.show_items_search_results = true
      $scope.items_search_results = Item.search(
        tags: tag
      )

    # =========== Infinite scrolling for posts ===========
    infinite_scroll_posts = new InfiniteScroll(Post)
    $scope.load_posts = ()->
      # Disable infinite scroll while loading
      $scope.layout.loading.posts = true
      infinite_scroll_posts.config(
        model_types: ["Post"]       # Expected model types from the backend
        init_starts: $scope.numOfPosts
      )
      $scope.posts = infinite_scroll_posts.load($scope.posts)
      $scope.posts.$asPromise().then (response)->
        # Success handlers
        infinite_scroll_posts.success_handler(response)
        $scope.layout.loading.posts = false
      , ()->
        # Error handlers
        Alert.show_msg("All posts are downloaded ...")

    # =========== Infinite scrolling for items ===========
    infinite_scroll_items = new InfiniteScroll(Item)
    infinite_scroll_items.config(
      model_types: ["Item"]       # Expected model types from the backend
      init_starts: $scope.items.length
    )
    $scope.load_items = ()->
      $scope.layout.loading.items = true
      $scope.items = infinite_scroll_items.load($scope.items)
      $scope.items.$asPromise().then (response)->
        infinite_scroll_items.success_handler(response)
        $scope.layout.loading.items = false
      , ()->
        Alert.show_msg("All items are downloaded ...")

    # =========== Infinite scrolling for feeds ===========
    infinite_scroll_feeds = new InfiniteScroll(Feed)
    $scope.load_feeds = ()->
      $scope.layout.loading.feeds = true
      infinite_scroll_feeds.config(
        model_types: ["ItemEditRecord", "Post", "Item"]
        init_starts: $scope.feed_starts
      )
      $scope.feeds = infinite_scroll_feeds.load($scope.feeds)
      $scope.feeds.$asPromise().then (response)->
        infinite_scroll_feeds.success_handler(response)
        $scope.layout.loading.feeds = false
      , ()->
        Alert.show_msg("All feeds are downloaded ...")


    infinite_scroll_timeline = new InfiniteScroll(Timeline)
    $scope.load_timeline = ()->
      $scope.layout.loading.timeline = true
      infinite_scroll_timeline.config(
        init_starts: $scope.timeline_starts
        model_types: ["Item", "ItemEditRecord", "ItemTransactionRecord"]
      )
      $scope.timeline = infinite_scroll_timeline.load($scope.timeline)
      $scope.timeline.$asPromise().then (response)->
        infinite_scroll_timeline.success_handler(response)
        $scope.layout.loading.timeline = false
      , ()->
        Alert.show_msg("All timeline events are downloaded ...")

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

]
