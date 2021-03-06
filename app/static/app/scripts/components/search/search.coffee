angular.module "worldsheet"


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
