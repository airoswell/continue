
angular.module("worldsheet")

.controller "userProfileCtrl", [
  "$scope", "Post", "Item", "Feed", "UserTimeline", "Alert",
  "InfiniteScroll", "Auth", "Album",
  ($scope, Post, Item, Feed, UserTimeline, Alert, InfiniteScroll, Auth, Album) ->

    $scope.layout = {
      creating_new_item: false
      display_tab: "timeline"
      show_items_search_results: false
      loading:
        "posts": false
        "timeline": false
        "items": true
    }

    $scope.$watch "user_id", ()->
      $scope.timeline = UserTimeline.$search(
        user_id: $scope.user_id
        num_of_records: 0
      ).$then (response)->
        $scope.layout.loading.timeline = false
        response.starts = $scope.timeline_starts

    # =========== Infinite scrolling for timeline ===========
    infinite_scroll_timeline = new InfiniteScroll(UserTimeline)
    $scope.load_timeline = ()->
      console.log "hah"
      $scope.layout.loading.timeline = true
      infinite_scroll_timeline.config(
        init_starts: $scope.timeline_starts
        model_types: ["ItemEditRecord", "ItemTransactionRecord"]
        extra_params:
          num_of_records: 8
      )
      $scope.timeline = infinite_scroll_timeline.load($scope.timeline)
      $scope.timeline.$asPromise().then (response)->
        infinite_scroll_timeline.success_handler(response)
        $scope.layout.loading.timeline = false
      , ()->
        Alert.show_msg("All timeline events are downloaded ...")

    # =========== Infinite scrolling for posts ===========
    infinite_scroll_posts = new InfiniteScroll(Post)
    $scope.load_posts = ()->
      # Disable infinite scroll while loading
      $scope.layout.loading.posts = true
      infinite_scroll_posts.config(
        model_types: ["Post"]       # Expected model types from the backend
        init_starts: $scope.numOfPosts
        extra_params:
          user_id: $scope.user_id
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
    $scope.load_first_items = ()->
      # Load the first few items when user click the `Gallery`
      if not $scope.items?
        Alert.show_msg("Downloading your data ...")
        $scope.items = Item.$search(
          num_of_records: 8
          # the user_id param will be use in all later queries, unless
          # otherwise specified, therefore no need to add <extra_params>
          # in later requests
          user_id: $scope.user_id
        ).$then (response)->
          this.tags_handler()       # Handle the tags and private-tags
          # set the start for future infinite scrolling
          this.start = this.length
          Alert.show_msg("Download is finished.")
          $scope.layout.loading.items = false
        , (e)->
          if e.$response.status == 404
            Alert.show_msg("No data is found.")
          else
            Alert.show_error("There is problem retrieving your data.")
    $scope.items_search = (tag)->
      Alert.show_msg("Searching...")
      $scope.layout.items_search_keyword = tag
      $scope.layout.show_items_search_results = true
      $scope.items_search_results = Item.search(
        tags: tag
      )
    infinite_scroll_items = new InfiniteScroll(Item)
    $scope.load_items = ()->
      infinite_scroll_items.config(
        model_types: ["Item"]       # Expected model types from the backend
        init_starts: $scope.items.length
        user_id: $scope.user_id
      )
      $scope.layout.loading.items = true
      $scope.items = infinite_scroll_items.load($scope.items)
      $scope.items.$asPromise().then (response)->
        infinite_scroll_items.success_handler(response)
        $scope.layout.loading.items = false
      , ()->
        Alert.show_msg("All items are downloaded ...")

    $scope.display_tab = (tab_name)->
      $scope.layout.display_tab = tab_name
      if tab_name == "items"
        $scope.load_first_items()
      if tab_name == "settings"
        profile = $scope.profile
        $scope.primary_area = profile.primary_area
        $scope.interested_areas_array = profile.interested_areas.split(",")
        $scope.interested_areas_tags = [{text: tag} for tag in $scope.interested_areas_array][0]

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
      item.owner = Auth.get_profile().id
      item.is_new = true
      $scope.items.splice 0, 0, item
      $("html, body").animate scrollTop: $("#items-display").offset().top - 100
      true

    $scope.change_profile_photo = ()->
      Album.get_albums().then (response)->
        $scope.profile.social_account_photo = response
        $scope.profile.$save()
]
