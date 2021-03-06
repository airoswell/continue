angular.module("worldsheet")


.directive "postOverview", ->
  restrict: "E"
  templateUrl: "/static/app/directives/post-overview.html"

.directive "dashboardItemOverview", ["Album", "Alert", (Album, Alert)->
  restrict: "E"
  scope: true
  templateUrl: "/static/app/directives/dashboard-item-overview.html"
  link: (scope, element, attrs) ->
    
    element.on "click", (e)->
      if "trigger" of e.target.attributes
        scope.expand(scope.item)
        scope.$apply()
]

.directive "angularItemUpdate", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/angular-item-update.html"

.directive "inputText", ->
  restrict: "E"
  templateUrl: "/static/app/directives/input-text.html"
  scope:
    data: "="
    label: "="
    placeHolder: "="
    inputClass: "="
    containerClass: "="

.directive "inputDropdown", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-dropdown.html"
  scope:
    data: "="
    label: "="
    choices: "="
    containerClass: "="
    transfer: "="
    user: "="
  link: (scope, element, attrs) ->
    scope.dropdown = false
    trigger = element.find("[trigger]")
    trigger
    .on("click", () ->
      scope.dropdown = true
      min_width = element.width()
      console.log "min_width", min_width
      trigger.find("[target]").css({"min-width": min_width})
      scope.$apply()
    )
    .on("mouseleave", () ->
      scope.dropdown = false
      scope.$apply()
    )
    scope.select = (option) ->
      scope.data = option

.directive "inputTextarea", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-textfield.html"
  scope:
    data: "="
    label: "="
    containerClass: "@"
    inputClass: "@"
    placeHolder: "="

.directive "inputDate", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-date.html"
  replace: true
  scope:
    date: "="
    label: "@"

.directive "inputNum", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-num.html"
  scope:
    num: "="
    label: "@"
  link: (scope, element)->
    scope.click = ()->
      element.find("input").focus()
      true

.directive "donationSettingForm", ()->
  restrict: "A"

.directive "areaSettingForm", ["Auth", "Alert", (Auth, Alert)->
  restrict: "A"
  link: (scope, element, attrs)->

    validate = ()->
      for tag in scope.interested_areas_tags
        if not /^\d{5}$/.test(tag.text)
          return false
      return  true
    scope.submit_areas_setting = ()->
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
      profile.save().$then (response)->
        scope.hide_area_setting = true
        Alert.show_msg("Your data is saved.")
]