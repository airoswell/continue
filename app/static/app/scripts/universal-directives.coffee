angular.module("continue")

.filter "requested", ()->
  return (user_id, item)->
    requesters_id = [requester.id for requester in item.requesters]
    if user_id in requesters_id
      return true
    return false

.filter "previously_owned", ()->
  return (user_id, item)->
    return user_id in item.previous_owners

.directive "postOverview", ["PrivateMessage", (PrivateMessage)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.items = []
    post_id = attrs["postId"]
    owner_id = attrs['ownerId']
    element.find("[contact-button]").css({"display": ""})
    scope.contact = ()->
      PrivateMessage.compose(owner_id, post_id, scope.items)
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
      console.log "auto_expand"
      size = Math.floor(data.toString().length/5) * 5 + 6
      if data == "Tall"
        console.log "data = ", data
        console.log size
      if size > scope.minSize
        input.css({"width": "auto"})
        input.attr({"size": size})

    input = element.find("input")
    # <data> should be the content of the input
    scope.$watch "data", ()->
      # sometimes AngularJS was not fast enough to pull in the template,
      # and therefore unable to define input; so redefine it.
      if input.length == 0
        input = element.find("input")
      if not scope.data
        input.css({"width": scope.initWidth, "max-width": "500px"})
      if scope.data
        auto_expand(scope.data)

# Use to expand post-detail
# [max-height] attribute use to control initial max-height
.directive "clickToExpand", ()->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.expanded = false
    max_height = "0px"
    if "maxHeight" of attrs
      max_height = attrs['maxHeight']
    trigger = element.find("[click-to-expand-trigger]")
    trigger.css({"cursor": "pointer"})
    target = element.find("[click-to-expand-target]")
    target.css({'max-height': max_height, "display": "none"})
    trigger.on "click", ()->
      if not scope.expanded
        target.css({"max-height": "", "display": "inherit"})
        scope.expanded = true
        scope.$apply()
      else if (scope.expanded)
        target.css({"max-height": max_height, "display": "none"})
        scope.expanded = false
        scope.$apply()


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
  scope: true
  link: (scope, element, attrs)->
    scope.click_to_show_is_show = false
    trigger = element.find("[click-to-show-trigger]")
    target = element.find("[click-to-show-target]")
    target.css({"display":"none"})
    trigger.on "click", (e)->
      if "tag" in e.target.className.split(" ")
        return
      if not scope.click_to_show_is_show
        target.css({"display": ""})
      else if scope.click_to_show_is_show
        target.css({"display": "none"})
      scope.click_to_show_is_show = !scope.click_to_show_is_show
      scope.$apply()


.directive "togglePartialImg", ()->
  restrict: "A"
  link: (scope, element, attrs)->
    max_height = "300px"
    if "maxHeight" of attrs
      max_height = attrs['maxHeight']
    unwatch = scope.$watch "item.pic", ()->
      container = element.find(".image-container")
      container.css({"overflow": "hidden", "max-height": max_height})
      container.on "click", ()->
        if container.css("max-height") != "none"
          container.css({"max-height": "none"})
        else
          container.css({"max-height": max_height})
      unwatch()

.directive "followButtonArea", ["Auth", "Alert", (Auth, Alert)->
  restrict: "A"
  link: (scope, element, attrs)->
    area = attrs['area']
    scope.is_followed = (area)->
      area_regex = RegExp(area)
      area_regex.test(scope.profile.interested_areas)
    scope.follow = (area)->
      if not scope.is_followed(area)
        profile = Auth.get_profile()
        profile.interested_areas += ",#{area}"
        profile.$save().$then (response)->
          Alert.show_msg("Successfully followed #{area}")
]


.directive "angularItemEditMenu", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/angular-item-edit-menu.html"
  link: (scope, element, attrs)->
    scope.refresh = false
    if "refresh" in attrs
      scope.refresh = attrs["refresh"]


.directive "itemEditButton", ["ItemEditor", "$rootScope", (ItemEditor, $rootScope)->
  restrict: "A"
  link: (scope, element, attrs)->
    # Initialize the button
    if "itemId" of attrs
      item_id = attrs['itemId']
    refresh = false
    if "refresh" of attrs
      refresh = attrs['refresh']

    scope.show_editor = ()->
      # refresh parameter signals that if the window is refreshed
      # after ItemEditor.deferred is resolved
      if item_id
        # Called inside django-item-edit-menu
        # where scope.item is not ready
        promise = ItemEditor.begin(item_id, refresh)
      else
        # Called inside angular-item-edit-menu
        # scope.item is already there from ng-repeat="item in ..."
        scope.item.is_new = false
        promise = ItemEditor.begin(scope.item, refresh)

      promise.then (response)->
        if scope.view == "post"
          console.log "We are in view post!!!"
          existing_items = scope.post.items
          console.log "scope.post.items", scope.post.items
          for i in [0...existing_items.length]
            console.log "existing_items[#{i}]", existing_items[i]
            if existing_items[i].id == response.id
              existing_items[i] = response
          console.log "After the update, scope.post.items = ", scope.post.items
]

.directive "dropDownMenu", ["$timeout", ($timeout)->
  restrict: "A"
  # scope: true
  link: (scope, element, attrs)->
    trigger = element.find("[drop-down-menu-trigger]")
    target = element.find("[drop-down-menu-target]")
    target.css({"position": "absolute", "display": "none", "z-index": 1})

    trigger.on "click", (e)->
      target.css({"display": ""})
      console.log "clicked!"
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


# Add extra transfer functionality to the drop-down-menu
.directive "transferMenu", ["Item", (Item)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.new_owner = undefined
    item_id = attrs["itemId"]
    item = Item.$find(item_id)
    scope.transfer = ()->
      item.new_owner = scope.new_owner
      console.log "transferring", scope.item
      item.save()
      # location.reload()
    scope.select = (requester_id, requester_name)->
      scope.new_owner = {
        id: requester_id
        username: requester_name
      }
]


.directive "itemTitle", ()->
  restrct: "E"
  scope:
    item: "="
  templateUrl: "/static/app/directives/item-title.html"
  link: (scope, element, attrs)->
    console.log "itemTitle"

.directive "angularItemOverviewHeader", ()->
  restrct: "E"
  templateUrl: "/static/app/directives/angular-item-overview-header.html"

.directive "angularItemOverview", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/angular-item-overview.html"

.directive "angularFieldText", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/angular-field-text.html"
  replace: true
  scope: {}
  link: (scope, element, attrs)->
    scope.widget = "text"
    scope.title = attrs["title"]
    scope.value = attrs['value']
    if "widget" of attrs
      scope.widget = attrs['widget']
    if 'unit' of attrs
      scope.unit = attrs['unit']
