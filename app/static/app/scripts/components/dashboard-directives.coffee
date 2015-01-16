angular.module("continue")

.directive "dashboardHistoryOverview", ->
  restrict: "E"
  templateUrl: "/static/app/directives/dashboard-history-overview.html"
  link: (scope, element, attrs) ->
      return

.directive "postOverview", ->
  restrict: "E"
  templateUrl: "/static/app/directives/post-overview.html"

.directive "dashboardItemOverview", ["History", "Album", "Alert", (History, Album, Alert)->
  restrict: "E"
  scope: true
  templateUrl: "/static/app/directives/dashboard-item-overview.html"
  link: (scope, element, attrs) ->
    scope.save = (item, handler)->
      console.log item.tags_input
      tags = [tag.text for tag in item.tags_input][0].join(",")
      item.tags = tags
      item.save(handler)
    scope.expand = (item) ->
      console.log "item.expanded isnt true", item.expanded isnt true
      if item.expanded isnt true
        console.log "expand"
        item.expanded = true
        item.histories = item.histories.$search({num_of_records: 8})
      else
        console.log "fold"
        item.expanded = false
        item.histories = History
      return

    scope.get_albums = (item)->
      Alert.show_msg("Downloading your albums ...")
      Album.get_albums().then (response)->
        item.pic = response

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
    element.find("[trigger]")
    .on("click", () ->
      scope.dropdown = true
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

