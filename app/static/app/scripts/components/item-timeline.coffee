angular.module "continue"

.controller "itemTimelineCtrl", [
  "$scope", "InfiniteScroll", "ItemTimeline"
  ($scope, InfiniteScroll, ItemTimeline)->

    console.log "itemTimelineCtrl"

    infinite_scroll_timeline = new InfiniteScroll(ItemTimeline)
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


]