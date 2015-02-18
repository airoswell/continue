
angular.module("continue")

.filter "orderByField", ["Item", (Item)->
  return (collection, type, order_by)->
    if type == 'field'
      console.log "order_by = ", order_by
      order_by = Item.customized_fields_normalization(order_by)
    return collection
]
.controller "collectionCtrl", [
  "$scope", "Item", "Alert", "InfiniteScroll", "Auth",
  ($scope, Item, Alert, InfiniteScroll, Auth) ->

    $scope.items_search_results = []
    $scope.layout = {
      # Control the currently loaded item list
      creating_new_item: false
      item_to_edit: {}
      filter_available: ""
      view_mode: "detail"
      # Control the display of search result, including ordering
      items_search_results_order_by_type: ""
      items_search_results_order_by: ""
      show_items_search_results: false
      search_result_not_found: false
      loading:          # To control infinite-scroll
        "items": true
    }
    $scope.tags = []    # A list of tags that will be searched against

    $scope.switch_view_mode = (mode)->
      $scope.layout.view_mode = mode

    # Filter the currently loaded items according to availability
    $scope.filter_available = (option)->
      if $scope.layout.filter_available == option
        $scope.layout.filter_available = ""
      else
        $scope.layout.filter_available = option

    $scope.edit_item = (item)->
      if item != $scope.layout.item_to_edit
        $scope.layout.item_to_edit = item
      else
        $scope.layout.item_to_edit = {}

    $scope.load_first_items = ()->
      # Load the first few items when user click the `Gallery`
      if not $scope.items?
        Alert.show_msg("Downloading your data ...")
        $scope.items = Item.search({num_of_records: 8}).$then (response)->
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
        $scope.layout.show_items_search_results = true
      else
        $scope.items_search_results = []
        $scope.layout.show_items_search_results = false

    $scope.search_by_field = (field)->
      params = {
        order_by: field.title
        order_by_model: field.model_name
      }
      model_name = Item.customized_fields_normalization(field).model_name
      search(params).$asPromise().then (response)->
        for item in response
          f = _.find(item[model_name], {"title": field.title})
          item['order_by_value'] = f.value
        $scope.layout.items_search_results_order_by = field
        $scope.layout.items_search_results_order_by_type = 'field'
        $scope.layout.show_items_search_results = true

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
      $scope.layout.show_items_search_results = false
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
