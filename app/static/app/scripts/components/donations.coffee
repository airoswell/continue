console.log "donations"

angular.module "continue"

.controller "donationsCtrl", [
  "$scope", "Item", "BulkItems", "Alert",
  ($scope, Item, BulkItems, Alert)->



    $scope.layout = {
      display_tab: 0
      success: false
      submitted: false
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
        title: "Donor's address"
        value: ""
      },
      {
        title: "Donor's zip code"
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
      {
        title: "Donor's pick-up info"
        value: ""
      },
      {
        title: "Donor's preferred pick-up date"
        value: ""
      },

    ]


    $scope.$watch "collector_uid", ()->
      item = Item.$build(Item.init)
      item.owner = $scope.collector_uid
      item.type = "donation"
      if $scope.categories.length > 0
        item.title = "Please select a type below"
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

    $scope.$watch "items", (newVal)->
      $('textarea').autosize()
    , true

    $scope.add_item = ()->
      item = Item.$build(Item.init)
      item.owner = $scope.collector_uid
      item.type = "donation"
      if $scope.categories.length > 0
        item.title = "Please select a type below"
      item.customized_num_fields = []
      item.customized_num_fields.push(
        {
          title: "Age"
          unit: "year"
          value: 0
        },
      )
      $scope.items.push(item)
      index = $scope.items.indexOf(item)
      $scope.layout.display_tab = index


    $scope.is_valid = ()->
      if not $scope.items
        Alert.show_msg("Please add at least one item.", 10000)
        return false
      for item in $scope.items
        if item.title == "Please select a type below"
          Alert.show_msg("Please specify types for all items.")
      if not $scope.contactForm.$valid
        Alert.show_msg("Please fill in your name and area")
        return false
      if (not $scope.customized_char_fields[3].value and
          not $scope.customized_char_fields[4].value)
        Alert.show_msg("Please provide either your phone number or your email address.")
        return false
      else if not $scope.customized_char_fields[3].value
        pat = /\d{3}[^0-9]*\d{3}[^0-9]*\d{4}$/
        is_valid = pat.test($scope.customized_char_fields[3].value)
        if not is_valid
          Alert.show_msg("Please provide valid phone number")
          return false
      return true

    $scope.submit = ()->
      console.log "submitting"
      if not $scope.is_valid()
        return
      for item in $scope.items
        if item.quantity == "5 +"
          item.quantity = 6
        if $scope.categories.length > 0
          item.tags = item.title
        item.customized_char_fields =  $scope.customized_char_fields
      $scope.bulk_items.items = $scope.items
      $scope.layout.submitted = true
      Alert.show_msg("Submitting your data ...")
      $scope.bulk_items.$save().$then (response)->
        console.log response
        $scope.received_items = response.items
        Alert.show_msg("Successfully submitted your data.")
        $scope.items = []
        $scope.layout.success = true


]