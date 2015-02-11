angular.module "continue"


.controller "SearchResultsCtrl", [
  "$scope", "Post", "Alert", "InfiniteScroll",
  ($scope, Post, Alert, InfiniteScroll)->

    $scope.scroll_to_post = (id)->
      console.log id
      # console.log "#post-#{id}"
      top = $("#post-#{id}").offset().top
      $("html, body").animate scrollTop: top - 100
      true

    $scope.layout = {
      loading:
        posts: false
    }

    infinite_scroll_posts = new InfiniteScroll(Post)
    $scope.load_posts = ()->
      # Disable infinite scroll while loading
      $scope.layout.loading.posts = true
      infinite_scroll_posts.config(
        model_types: ["Post"]       # Expected model types from the backend
        init_starts: $scope.init_post_num
        extra_params: {
          q: $scope.q,
          tags: $scope.tags,
          areas: $scope.areas,
          secret_key: $scope.secret_key,
        }
      )
      $scope.posts = infinite_scroll_posts.load(
        $scope.posts
      )
      $scope.posts.$asPromise().then (response)->
        # Success handlers
        infinite_scroll_posts.success_handler(response)
        $scope.layout.loading.posts = false
      , ()->
        # Error handlers
        Alert.show_msg("All posts are downloaded ...")
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
      
