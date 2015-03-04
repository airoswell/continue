angular.module "worldsheet"

.controller "itemTimelineCtrl", [
  "$scope", "InfiniteScroll", "ItemTimeline", "Update", "Alert",
  ($scope, InfiniteScroll, ItemTimeline, Update, Alert)->

    # Prevent the infinite scroll to load at the beginning.
    $scope.layout = {
      loading:
        timeline: true
      display_section: "timeline"
      display_record: undefined
      display_records: []
    }

    $scope.field_records_dict = {}

    $scope.$watch "item_id", ()->
      $scope.timeline = ItemTimeline.$search(
        item_id: $scope.item_id
        num_of_records: 0
      ).$then (response)->
        $scope.layout.loading.timeline = false
        console.log "$scope.init_starts", $scope.init_starts
        response.starts = $scope.init_starts


    infinite_scroll_timeline = new InfiniteScroll(ItemTimeline)

    $scope.load_timeline = ()->
      $scope.layout.loading.timeline = true
      console.log "$scope.timeline.starts", $scope.timeline.starts
      infinite_scroll_timeline.config(
        init_starts: $scope.init_starts
        model_types: ["ItemEditRecord", "ItemTransactionRecord"]
        extra_params:
          num_of_records: 8
      )
      $scope.timeline = infinite_scroll_timeline.load($scope.timeline)
      $scope.timeline.$asPromise().then (response)->
        console.log "response", response
        infinite_scroll_timeline.success_handler(response)
        $scope.layout.loading.timeline = false
      , ()->
        Alert.show_msg("All timeline events are downloaded ...")

    $scope.add_field = (field_title)->
      Alert.show_msg("Downloading your data ...")
      $scope.layout.display_section = "field-records"
      field_record = Update.$search(
        item_id: $scope.item_id
        field: field_title
      )
      $scope.field_records_dict[field_title] = (field_record)
      field_record.$then (response)->
        console.log "response", response
        Alert.show_msg("Done.")
      , (e)->
        console.log "error"


    $scope.clear = ()->
      $scope.layout.display_section = "timeline"
      $scope.field_records_dict = {}

    $scope.is_displaying = (field_title)->
      if field_title of $scope.field_records_dict
        return true
      false

]