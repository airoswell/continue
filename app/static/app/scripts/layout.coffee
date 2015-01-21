# Enable [tab] to indent
textareas = document.getElementsByTagName("textarea")
count = textareas.length
i = 0

while i < count
  textareas[i].onkeydown = (e) ->
    if e.keyCode is 9 or e.which is 9
      e.preventDefault()
      s = @selectionStart
      @value = @value.substring(0, @selectionStart) + "\t" + @value.substring(@selectionEnd)
      @selectionEnd = s + 1
    return
  i++

# Auto resize all textarea
$(document).ready ()->
  console.log "resizing"
  $('textarea').autosize()
  console.log $("textarea")
# ============================
angular.module("continue")

.controller "LayoutCtrl", [
  "$scope"
  "Auth"
  "Alert"
  ($scope, Auth, Alert) ->

    $scope.search = ()->
      areas = $scope.tags_to_string($scope.areas_tags)
      tags = $scope.tags_to_string($scope.tags_tags)
      $("input[name=areas]").val(areas)
      $("input[name=tags]").val(tags)
      document.getElementById('search-form').submit()
      # clear the input to prevent going back and see the input
      $("input").val("")
      return

    $scope.tags_to_string = (input_tags)->
      if input_tags
        areas = [tag.text for tag in input_tags]
        areas = areas.join(",")
        return areas
      return ""
    
    $("input[name='q'], input[name='secret_key']").keyup (e)->
      if e.which == 13
        $scope.search()
      return

    $scope.profile = {}
    $scope.scrollTop = 0
    angular.element($(window)).bind "scroll", ()->
      $scope.scrollTop = $(window).scrollTop()
      $scope.$apply()

    # Initialize user_info and modal data
    Auth.fetch_profile().then (response)->
      Auth.store_profile(response[0])
      $scope.profile = Auth.get_profile()
      $scope.photo = Auth.get_profile().social_account_photo

      
]

.directive "areaSettingForm", ["Auth", "Alert", (Auth, Alert)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->

    validate = ()->
      for tag in scope.interested_areas_tags
        if not /^\d{5}$/.test(tag.text)
          return false
      return  true
    scope.submit = ()->
      if not validate()
        Alert.show_error("Zip code can only contain 5 numeric digits.", 2000)
        return
      zip_codes = []
      for tag in scope.interested_areas_tags
        zip_codes.push(tag.text)
      scope.interested_areas = zip_codes.join() 
      console.log scope.interested_areas
      Alert.show_msg("Submitting ...")
      profile = Auth.get_profile()
      profile.primary_area = scope.primary_area
      profile.interested_areas = scope.interested_areas
      profile.already_set = true
      profile.$save().$then (response)->
        scope.hide_area_setting = true
        Alert.show_msg("Your data is saved.")
]


.filter "truncate", ()->
  return (input, max)->
    return input.slice(0, max)


.directive "transaction", ["Transaction", (Transaction)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    transaction_id = attrs["transactionId"]
    scope.transaction = Transaction.$find(transaction_id)
]