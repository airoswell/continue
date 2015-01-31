console.log "donations"

angular.module "continue"

.controller "donationsCtrl", [
  "$scope", "Item", "BulkItems", "Alert",
  ($scope, Item, BulkItems, Alert)->


    $scope.layout = {
      display_tab: 0
    }
    $scope.bulk_items = BulkItems.$build()
    $scope.items = []
    $scope.items_title = []
    $scope.items_tag = []

    $scope.customized_char_fields = [
      {
        title: "Donor's name"
        value: ""
      },
      {
        title: "Donor's area"
        value: ""
      },
      {
        title: "Donor's phone"
        value: ""
      },
      {
        title: "Donor's email"
        value: ""
      },
    ]

    item = Item.$build(Item.init)
    item.owner = $scope.collector_uid
    item.type = "donation"
    item.customized_num_fields = []
    item.customized_num_fields.push(
      {
        title: "Age"
        unit: "year"
        value: 0
      },
    )
    $scope.items.push(item)
    $scope.items_title.push(item.title)

    # $scope.$watch "items_tag", ()->
    #   for tag in $scope.items_tag
    #     if not (tag.text in $scope.items_title)
    #       item = Item.$build(Item.init)
    #       item.title = tag.text
    #       item.owner = $scope.collector_uid
    #       item.type = "donation"
    #       item.customized_num_fields = []
    #       item.customized_num_fields.push(
    #         {
    #           title: "Age"
    #           unit: "year"
    #           value: 0
    #         },
    #       )
    #       $scope.items.push(item)
    #       $scope.items_title.push(item.title)
    #     $scope.step_one_done = true
    # , true


    $scope.$watch "items", (newVal)->
      $('textarea').autosize()
    , true


    $scope.add_item = ()->
      item = Item.$build(Item.init)
      $scope.items.push(item)


    $scope.is_valid = ()->
      if not $scope.contactForm.$valid
        Alert.show_msg("Please fill in your name and area")
        return false
      if (not $scope.customized_char_fields[2].value and
          not $scope.customized_char_fields[3].value)
        Alert.show_msg("Please provide either your phone number or your email address.")
        return false
      else if not $scope.customized_char_fields[3].value
        pat = /\d{3}[^0-9]*\d{3}[^0-9]*\d{4}$/
        is_valid = pat.test($scope.customized_char_fields[2].value)
        if not is_valid
          Alert.show_msg("Please provide valid phone number")
          return false
      return true

    $scope.submit = ()->
      console.log "submitting"
      if not $scope.is_valid()
        return
      for item in $scope.items
        console.log "appending item"
        item.customized_char_fields =  $scope.customized_char_fields
      $scope.bulk_items.items = $scope.items
      Alert.show_msg("Submitting your data ...")
      $scope.bulk_items.$save().$then (response)->
        console.log response
        Alert.show_msg("Successfully submitted your data.")


]