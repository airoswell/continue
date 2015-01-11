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

angular.module("continue")

.controller "LayoutCtrl", [
  "$scope"
  "Auth"
  "Alert"
  ($scope, Auth, Alert) ->

    $scope.user = {}

    # Initialize user_info and modal data
    Auth.get_user_profile().then (response)->
      Auth.store_user(response[0])
      $scope.user = Auth.get_user()
      $scope.photo = Auth.get_user().social_account_photo
      
]


.directive "autoExpand", ->
  """
  <div auto-expand data="<the input variable>" init-width="100px"
      min-size="20">
      ...
      <input tyle='text' ng-model="<the input variable>">
  </div>
  """
  restrict: "AE"
  scope:
    data: "="
    minSize: "@"    # Static (one-way data-binding) use @
    initWidth: "@"  # otherwise errors [Non-Assignable Expression] shows
  link: (scope, element, attrs) ->
    # A function that auto expand the child input
    if scope.minSize == undefined
      scope.minSize = 7
    if scope.initWidth == undefined
      scope.initWidth = "80px"
    auto_expand = (data) ->
      size = Math.floor(data.toString().length/5) * 5 + 6
      if size > scope.minSize
        input.attr({"size": size})
        input.css({"width": "auto"})

    input = element.find("input")
    # <data> should be the content of the input
    scope.$watch "data", ()->
      # sometimes AngularJS was not fast enough to pull in the template,
      # and therefore unable to define input; so redefine it.
      if input.length == 0
        input = element.find("input")
      if not scope.data
        input.css({"width": scope.initWidth})
      if scope.data
        auto_expand(scope.data)


.directive "clickToShow", ()->
  """ template
  <div click-to-show>
    <div click-to-show-trigger></div>
    <div click-to-show-target></div>
  </div>
  clicking the '[click-to-show-trigger]' will show and hide
  '[click-to-show-trigger]'.
  """
  restrict: "A"
  scope: {}
  link: (scope, element, attrs)->
    scope.expanded = false
    trigger = element.find("[click-to-show-trigger]")
    target = element.find("[click-to-show-target]")
    target.css({"display":"none"})
    trigger.on "click", (e)->
      if not scope.expanded
        target.css({"display": ""})
      else if scope.expanded
        target.css({"display": "none"})
      scope.expanded = !scope.expanded
      scope.$apply()


.directive "itemEditMenu", (ItemEditor)->
  restrict: "E"
  templateUrl: "/static/app/directives/item-edit-menu.html"

.directive "itemEditButton", ["ItemEditor", (ItemEditor)->
  restrict: "A"
  link: (scope, element, attrs)->
    if "itemId" of attrs
      item_id = attrs['itemId']
    scope.show_editor = ()->
      console.log "show_editor"
      if item_id != "{{"
        ItemEditor.begin(item_id)
      else
        scope.item.is_new = false
        ItemEditor.begin(scope.item)
      
]

.directive "dropDownMenu", ["$timeout", ($timeout)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    trigger = element.find("[drop-down-menu-trigger]")
    target = element.find("[drop-down-menu-target]")
    target.css({"position": "absolute", "display": "none"})

    trigger.on "click", (e)->
      target.css({"display": ""})
    $("html").click (a)->
      if not $.contains(element[0], a.target)
        target.css({"display": "none"})
]

.directive "postItemDeleteButton", ["Item", (Item)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    item_id = attrs["itemId"]
    post_id = attrs["postId"]
    scope.show_double_check = false
    scope.double_check = ()->
      console.log "double_check scope", scope
      scope.show_double_check = true
    scope.del = ()->
      console.log "del"
      console.log "del scope", scope
      scope.show_double_check = false
      item = Item.$find(item_id).$then (response)->
        item.remove_from_post = post_id
        item.save()
]