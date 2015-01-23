angular.module "continue"

.controller "itemTimelineCtrl", [
  "$scope", "InfiniteScroll", "ItemTimeline", "Alert",
  ($scope, InfiniteScroll, ItemTimeline, Alert)->

    # Prevent the infinite scroll to load at the beginning.
    $scope.layout = {
      loading:
        timeline: true
    }

    $scope.$watch "item_id", ()->
      $scope.timeline = ItemTimeline.$search(
        pk: $scope.item_id
        num_of_records: 0
      ).$then (response)->
        $scope.layout.loading.timeline = false


    infinite_scroll_timeline = new InfiniteScroll(ItemTimeline)

    $scope.load_timeline = ()->
      $scope.layout.loading.timeline = true
      infinite_scroll_timeline.config(
        init_starts: $scope.init_starts
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


]