angular.module "continue"


.controller "SearchResultsCtrl", [
  "$scope", "Post", "Alert", ($scope, Post, Alert)->

    $scope.scroll_to_post = (id)->
      top = $("#post-#{id}").offset().top
      $("html, body").animate scrollTop: top - 100
      true

    $scope.layout = {
      loading:
        posts: false
        feeds: false
    }

    $scope.load_posts = ()->
      $scope.layout.loading.posts = true
      if not $scope.posts
        $scope.posts = Post.search(
          "start": $scope.init_post_num
          "q": $scope.q
          "area": $scope.area
        )
      else
        $scope.posts = $scope.posts.fetch(
          "start": $scope.posts.start
          "q": $scope.q
          "area": $scope.area
        )
      $scope.posts.$then (response)->
        # store the next [start] param; it will propagate to
        # queryset[start:end]65
        if $scope.posts.start == 0
          $scope.posts.start = parseInt($scope.init_post_num) + response.length
        else
          $scope.posts.start = parseInt($scope.posts.start) + response.length
        # Deal with the tags
        for post in response
          if post.tags
            if typeof(post.tags) == "string"
              post.tags = post.tags.split(",")
          else
            post.tags = []
          for item in post.items
            if item.tags
              if typeof(item.tags) == "string"
                item.tags = item.tags.split(",")
              else
                item.tags = []
      .$asPromise().then ()->
        $scope.layout.loading.posts = false
      , ()->
        Alert.show_msg("All posts are loaded above.")
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
      PrivateMessage.compose(owner_id, post_id, scope.items)
]

.directive "itemOverview", ()->
  restrict: "A"
  scope: true
  link: (scope, element, attrs)->
    scope.item_id = attrs['itemId']
    scope.add_item = ()->
      if not (scope.item_id in scope.items)
        scope.items.push(scope.item_id)
      else
        scope.items.splice scope.items.indexOf(scope.item_id), 1


# .directive "clickToShowTrigger", ()->
#   restrict: "A"
#   link: (scope, element, attrs)->
#     scope.expanded = false
#     click_to_show = element.find("[click-to-show]")
#     click_to_show.css({"display":"none"})
#     element.on "click", (e)->
#       if not scope.expanded
#         click_to_show.css({"display": "inherit"})
#       else if scope.expanded and not ("click-to-show" of e.target.attributes)
#         click_to_show.css({"display": "none"})
#       scope.expanded = !scope.expanded
#       scope.$apply()

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
    item = Item.$find(item_id)
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
