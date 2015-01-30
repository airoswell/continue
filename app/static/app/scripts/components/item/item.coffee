angular.module "continue"

.controller "itemCtrl", [
  "$scope", "Alert", "BulkItems", "Item", "Auth",
  ($scope, Alert, BulkItems, Item, Auth)->
    $scope.layout = {
      display_tab: 0
    }
    $scope.bulk_items = BulkItems.$build()
    $scope.items = []
    $scope.items_title = []
    $scope.items_tag = []

    $scope.add_item = ()->
      item = Item.$build(Item.init)
      $scope.items.push(item)

    $scope.remove = (item)->
      items = $scope.items
      index = items.indexOf(item)
      items.splice index, 1
      if index > 0
        $scope.layout.display_tab = index - 1
      else
        $scope.layout.display_tab = 0
    
    $scope.$watch "items_tag", ()->
      for tag in $scope.items_tag
        if not (tag.text in $scope.items_title)
          item = Item.$build(Item.init)
          item.title = tag.text
          item.owner = Auth.get_profile().id
          item.type = "normal"
          $scope.items.push(item)
          $scope.items_title.push(item.title)
    , true

    $scope.$watch "items", (newVal)->
      $('textarea').autosize()
    , true

    $scope.is_valid = ()->
      console.log $scope.items.length < 1
      if $scope.items.length < 1
        return false
      for item in $scope.items
        if not item.is_valid()
          return false
      return true

    $scope.submit = ()->
      if not $scope.is_valid()
        Alert.show_error("There are no items or necessary info are not provided.")
        return
      for item in $scope.items
        tags = [tag.text for tag in item.tags_input][0].join(",")
        tags_private = [tag.text for tag in item.tags_private_input][0].join(",")
        item.tags = tags
        item.tags_private = tags_private
      $scope.bulk_items.items = $scope.items
      Alert.show_msg("Submitting your data ...")
      $scope.bulk_items.$save().$then (response)->
        console.log response
        Alert.show_msg("Successfully submitted your data.")
        $scope.items = []
        window.location.replace("/app/user/dashboard/")

]