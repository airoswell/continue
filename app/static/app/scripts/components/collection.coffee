
angular.module("continue")

.controller "collectionCtrl", [
  "$scope", "Post", "Item", "Feed", "Timeline", "Alert",
  "InfiniteScroll", "Auth", "Album",
  ($scope, Post, Item, Feed, Timeline, Alert, InfiniteScroll, Auth, Album) ->


    $scope.layout = {
      creating_new_item: false
      display_tab: "items"
      view_mode: "detail"
      item_to_edit: {}
      show_items_search_results: false
      search_result_not_found: false
      loading:
        "items": true
    }
    $scope.tags = []    # A list of tags that will be searched against

    $scope.switch_view_mode = (mode)->
      $scope.layout.view_mode = mode

    $scope.edit_item = (item)->
      if item != $scope.layout.item_to_edit
        $scope.layout.item_to_edit = item
      else
        $scope.layout.item_to_edit = {}

    $scope.load_first_items = ()->
      # Load the first few items when user click the `Gallery`
      if not $scope.items?
        Alert.show_msg("Downloading your data ...")
        $scope.items = Item.$search({num_of_records: 8}).$then (response)->
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

    $scope.load_first_items()

    # =========== Infinite scrolling for items ===========
    infinite_scroll_items = new InfiniteScroll(Item)
    $scope.load_items = ()->
      console.log "$scope.items", $scope.items
      console.log "$scope.items.length", $scope.items.length
      infinite_scroll_items.config(
        model_types: ["Item"]       # Expected model types from the backend
        init_starts: $scope.items.length
      )
      $scope.layout.loading.items = true
      $scope.items = infinite_scroll_items.load($scope.items)
      $scope.items.$asPromise().then (response)->
        infinite_scroll_items.success_handler(response)
        $scope.layout.loading.items = false
      , ()->
        Alert.show_msg("All items are downloaded ...")

    search = (params)->
      $scope.layout.search_result_not_found = false
      Alert.show_msg("Searching...")
      $scope.layout.show_items_search_results = true
      $scope.items_search_results = Item.search(
        params
      ).$then ()->
        console.log "success"
      , (e)->
        if e.$response.status = 404
          $scope.items_search_results = []
          $scope.layout.search_result_not_found = true
          Alert.show_msg("There is no item matching the criteria.")

    $scope.search_by_tag = (tag)->
      if tag in $scope.tags
        index = $scope.tags.indexOf(tag)
        $scope.tags.splice index, 1
      else
        $scope.tags.push(tag)
      if $scope.tags.length > 0
        tags = $scope.tags.join(",")
        params = {"tags": tags}
        search(params)
      else
        $scope.items_search_results = []

    $scope.is_searched = (tag)->
      tag in $scope.tags

    $scope.creating_new_item = ()->
      if not ($scope.items?)
        return false
      items = $scope.items
      if items.length > 0
        for item in items
          if not ('id' of item)
            return true
      return false

    $scope.create_item = () ->
      if $scope.creating_new_item()
        return
      if not $scope.items?
        $scope.items = []
      $scope.layout.view_mode = "detail"
      $scope.layout.display_tab = "items"
      item = Item.$build(Item.init)
      item.owner = Auth.get_profile().id
      item.is_new = true
      $scope.items.splice 0, 0, item
      $("html, body").animate scrollTop: $("#items-display").offset().top - 100
      true
]


.directive "thumbnailItem", ()->
  restrict: "A"
  scope:
    item: "="
