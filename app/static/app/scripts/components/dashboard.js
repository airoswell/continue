// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("continue").controller("DashBoardCtrl", [
    "$scope", "Post", "Item", "Feed", "Alert", "Auth", function($scope, Post, Item, Feed, Alert, Auth) {
      Alert.show_msg("Downloading your data.");
      $scope.items = Item.$search({
        num_of_records: 8
      }).$then(function() {
        var item, tag, _i, _len, _ref;
        _ref = $scope.items;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          item = _ref[_i];
          if (item.tags) {
            item.tags_input = [
              (function() {
                var _j, _len1, _ref1, _results;
                _ref1 = item.tags.split(",");
                _results = [];
                for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
                  tag = _ref1[_j];
                  _results.push({
                    "text": tag
                  });
                }
                return _results;
              })()
            ][0];
          }
        }
        return Alert.show_msg("Download is finished.");
      });
      $scope.layout = {
        creating_new_item: false,
        display_tab: "timeline",
        loading: {
          "posts": false,
          "feeds": false,
          "timeline": false
        }
      };
      $scope.load_posts = function() {
        $scope.layout.loading.posts = true;
        if (!$scope.posts) {
          $scope.posts = Post.search({
            "start": $scope.numOfPosts
          });
        } else {
          $scope.posts = $scope.posts.fetch({
            "start": $scope.posts.start
          });
        }
        return $scope.posts.$then(function(response) {
          var post, _i, _len, _ref, _results;
          if ($scope.posts.start === 0) {
            $scope.posts.start = parseInt($scope.numOfPosts) + $scope.posts.length;
          } else {
            $scope.posts.start = parseInt($scope.numOfPosts) + $scope.posts.length;
          }
          _ref = $scope.posts;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            post = _ref[_i];
            if (post.tags) {
              if (typeof post.tags === "string") {
                _results.push(post.tags = post.tags.split(","));
              } else {
                _results.push(void 0);
              }
            } else {
              _results.push(post.tags = []);
            }
          }
          return _results;
        }).$asPromise().then(function() {
          return $scope.layout.loading.posts = false;
        }, function() {
          return Alert.show_msg("You have reach the end of the posts.");
        });
      };
      $scope.load_feeds = function() {
        $scope.layout.loading.feeds = true;
        if (!$scope.feeds) {
          $scope.feeds = Feed.$search({
            "feed_starts": $scope.feed_starts
          });
        } else {
          $scope.feeds = $scope.feeds.$fetch({
            "feed_starts": $scope.feeds.feed_starts
          });
        }
        return $scope.feeds.$then(function(response) {
          var feed, item, post, _i, _len, _ref, _results;
          console.log("response.length", response.length);
          $scope.feeds.feed_starts = $scope.feed_starts;
          _ref = $scope.feeds;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            feed = _ref[_i];
            if (feed.model_name === "Post") {
              $scope.feeds.feed_starts.Post += 1;
              post = feed;
              if (post.tags) {
                if (typeof post.tags === "string") {
                  post.tags = post.tags.split(",");
                }
              } else {
                post.tags = [];
              }
            }
            if (feed.model_name === "Item") {
              $scope.feeds.feed_starts.Item += 1;
              item = feed;
              if (item.tags) {
                if (typeof item.tags === "string") {
                  _results.push(item.tags = item.tags.split(","));
                } else {
                  _results.push(void 0);
                }
              } else {
                _results.push(item.tags = []);
              }
            } else if (feed.model_name === "ItemEditRecord") {
              _results.push($scope.feeds.feed_starts.ItemEditRecord += 1);
            } else {
              _results.push(void 0);
            }
          }
          return _results;
        }).$asPromise().then(function() {
          return $scope.layout.loading.feeds = false;
        }, function() {
          return Alert.show_msg("All feeds are already loaded.");
        });
      };
      $scope.load_timeline = function() {
        console.log("loading timeline");
        $scope.layout.loading.timeline = true;
        if (!$scope.timeline) {
          $scope.timeline = Feed.$search({
            "timeline_starts": $scope.timeline_starts
          });
        } else {
          $scope.timeline = $scope.timeline.$fetch({
            "timeline_starts": $scope.timeline.timeline_starts
          });
        }
        return $scope.timeline.$then(function(response) {
          var feed, item, _i, _len, _ref, _results;
          $scope.timeline.timeline_starts = $scope.timeline_starts;
          _ref = $scope.timeline;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            feed = _ref[_i];
            if (feed.model_name === "ItemTransactionRecord") {
              _results.push($scope.timeline.timeline_starts.ItemTransactionRecord += 1);
            } else if (feed.model_name === "Item") {
              $scope.timeline.timeline_starts.Item += 1;
              item = feed;
              if (item.tags) {
                if (typeof item.tags === "string") {
                  _results.push(item.tags = item.tags.split(","));
                } else {
                  _results.push(void 0);
                }
              } else {
                _results.push(item.tags = []);
              }
            } else if (feed.model_name === 'ItemEditRecord') {
              _results.push($scope.timeline.timeline_starts.ItemEditRecord += 1);
            } else {
              _results.push(void 0);
            }
          }
          return _results;
        }).$asPromise().then(function() {
          return $scope.layout.loading.timeline = false;
        });
      };
      $scope.display_tab = function(tab_name) {
        return $scope.layout.display_tab = tab_name;
      };
      $scope.scroll_to_post = function(id) {
        var top;
        top = $("#post-" + id).offset().top;
        $("html, body").animate({
          scrollTop: top - 100
        });
        return true;
      };
      $scope.create_item = function() {
        var item;
        if ($scope.layout.creating_new_item) {
          return;
        }
        $scope.layout.creating_new_item = true;
        $scope.layout.display_tab = "items";
        item = Item.$build(Item.init);
        item.is_new = true;
        $scope.items.splice(0, 0, item);
        $("html, body").animate({
          scrollTop: $("#items-display").offset().top - 100
        });
        return true;
      };
      $scope.create_post = function() {
        var post;
        if ($scope.layout.creating_new_post) {
          return;
        }
        layout.creating_new_post = true;
        post = Post.$build(Post.init);
        post.owner = Auth.get_user().user_id;
        $scope.posts.splice(0, 0, post);
        $("html, body").animate({
          scrollTop: $("#posts-display").offset().top - 100
        });
        return true;
      };
      $scope.item_update_successHandler = function(item, response) {
        item.expanded = false;
        return item.new_status = "";
      };
      $scope.item_create_successHandler = function(item, response) {
        layout.creating_new_item = false;
        item.expanded = false;
        item.is_new = false;
        item.new_status = "";
        return $scope.histories.$refresh();
      };
      $scope.post_create_successHandler = function(item, response) {
        layout.creating_new_post = false;
        return post.is_new = false;
      };
      $scope.post_update_successHandler = function(item, response) {
        return console.log("successfully updated the post.");
      };
      $scope.add_item = function(post) {
        return post.add_item();
      };
      return $scope.add_existing_item = function(post) {
        var item;
        item = post.add_item();
        return BottomSheet.show(item);
      };
    }
  ]);

}).call(this);
