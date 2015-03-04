
angular.module("worldsheet")

.controller "DashBoardCtrl", [
  "$scope", "Post", "Item", "Feed", "Timeline", "Alert",
  "InfiniteScroll", "Auth", "Album",
  ($scope, Post, Item, Feed, Timeline, Alert, InfiniteScroll, Auth, Album) ->


    $scope.layout = {
      creating_new_item: false
      display_tab: "feeds"
      show_items_search_results: false
      loading:
        "posts": false
        "feeds": false
        "timeline": false
    }


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
      if tab_name == "items"
        $scope.load_first_items()
      if tab_name == "settings"
        profile = $scope.profile
        $scope.interested_areas_array = []
        $scope.primary_area = profile.primary_area
        if profile.interested_areas.length > 0
          $scope.interested_areas_array = profile.interested_areas.split(",")
        $scope.interested_areas_tags = [{text: tag} for tag in $scope.interested_areas_array][0]

    $scope.scroll_to_post = (id)->
      top = $("#post-#{id}").offset().top
      $("html, body").animate scrollTop: top - 100
      true


    $scope.change_profile_photo = ()->
      Album.get_albums().then (response)->
        $scope.profile.social_account_photo = response
        $scope.profile.$save()
]
