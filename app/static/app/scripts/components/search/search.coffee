angular.module "continue"


.controller "SearchResultsCtrl", [
  "$scope", ($scope)->

    $scope.scroll_to_post = (id)->
      top = $("#post-#{id}").offset().top
      $("html, body").animate scrollTop: top - 100
      true
]



.directive "searchPostOverview", ["PrivateMessage", (PrivateMessage)->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.items = []
    post_id = attrs["postId"]
    owner_id = attrs['ownerId']
    element.find("[contact-button]").css({"display": ""})
    scope.contact = ()->
      console.log "scope.items", scope.items
      PrivateMessage.compose(owner_id, post_id, scope.items)
]

.directive "searchItemOverview", ()->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.item_id = attrs['itemId']
    scope.add_item = ()->
      if not (scope.item_id in scope.items)
        scope.items.push(scope.item_id)
      else
        scope.items.splice scope.items.indexOf(scope.item_id), 1


.directive "clickToShowTrigger", ()->
  restrict: "A"
  link: (scope, element, attrs)->
    scope.expanded = false
    click_to_show = element.find("[click-to-show]")
    click_to_show.css({"display":"none"})
    element.on "click", (e)->
      if not scope.expanded
        click_to_show.css({"display": "inherit"})
      else if scope.expanded and not ("click-to-show" of e.target.attributes)
        click_to_show.css({"display": "none"})
      scope.expanded = !scope.expanded
      scope.$apply()

.directive "clickToExpand", ()->
  restrict: "A"
  link: (scope, element, attrs)->
    scope.expanded = false
    max_height = attrs['maxHeight']
    trigger = element.find("[click-to-expand-trigger]")
    target = element.find("[click-to-expand-target]")
    trigger.on "click", ()->
      if not scope.expanded
        target.css({"max-height": ""})
        scope.expanded = true
      else if (scope.expanded)
        target.css({"max-height": max_height, "overflow": "hidden"})
        scope.expanded = false


# Add extra transfer functionality to the drop-down-menu
.directive "transferMenu", ["Item", (Item)->
  restrict: "A"
  link: (scope, element, attrs)->
    scope.new_owner = undefined
    item_id = attrs["itemId"]
    item = Item.$find(item_id).$then (response)->
      console.log item
    scope.transfer = ()->
      item.new_owner = scope.new_owner
      console.log "transferring", scope.item
      item.save()
      location.reload()
    scope.select = (requester_id, requester_name)->
      scope.new_owner = {
        id: requester_id
        username: requester_name
      }
]      
