// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("worldsheet").controller("userProfileCtrl", [
    "$scope", "Post", "Item", "Feed", "UserTimeline", "Alert", "InfiniteScroll", "Auth", "Album", function($scope, Post, Item, Feed, UserTimeline, Alert, InfiniteScroll, Auth, Album) {
      var infinite_scroll_items, infinite_scroll_posts, infinite_scroll_timeline;
      $scope.layout = {
        creating_new_item: false,
        display_tab: "timeline",
        show_items_search_results: false,
        loading: {
          "posts": false,
          "timeline": false,
          "items": true
        }
      };
      $scope.$watch("user_id", function() {
        return $scope.timeline = UserTimeline.$search({
          user_id: $scope.user_id,
          num_of_records: 0
        }).$then(function(response) {
          $scope.layout.loading.timeline = false;
          return response.starts = $scope.timeline_starts;
        });
      });
      infinite_scroll_timeline = new InfiniteScroll(UserTimeline);
      $scope.load_timeline = function() {
        console.log("hah");
        $scope.layout.loading.timeline = true;
        infinite_scroll_timeline.config({
          init_starts: $scope.timeline_starts,
          model_types: ["ItemEditRecord", "ItemTransactionRecord"],
          extra_params: {
            num_of_records: 8
          }
        });
        $scope.timeline = infinite_scroll_timeline.load($scope.timeline);
        return $scope.timeline.$asPromise().then(function(response) {
          infinite_scroll_timeline.success_handler(response);
          return $scope.layout.loading.timeline = false;
        }, function() {
          return Alert.show_msg("All timeline events are downloaded ...");
        });
      };
      infinite_scroll_posts = new InfiniteScroll(Post);
      $scope.load_posts = function() {
        $scope.layout.loading.posts = true;
        infinite_scroll_posts.config({
          model_types: ["Post"],
          init_starts: $scope.numOfPosts,
          extra_params: {
            user_id: $scope.user_id
          }
        });
        $scope.posts = infinite_scroll_posts.load($scope.posts);
        return $scope.posts.$asPromise().then(function(response) {
          infinite_scroll_posts.success_handler(response);
          return $scope.layout.loading.posts = false;
        }, function() {
          return Alert.show_msg("All posts are downloaded ...");
        });
      };
      $scope.load_first_items = function() {
        if ($scope.items == null) {
          Alert.show_msg("Downloading your data ...");
          return $scope.items = Item.$search({
            num_of_records: 8,
            user_id: $scope.user_id
          }).$then(function(response) {
            this.tags_handler();
            this.start = this.length;
            Alert.show_msg("Download is finished.");
            return $scope.layout.loading.items = false;
          }, function(e) {
            if (e.$response.status === 404) {
              return Alert.show_msg("No data is found.");
            } else {
              return Alert.show_error("There is problem retrieving your data.");
            }
          });
        }
      };
      $scope.items_search = function(tag) {
        Alert.show_msg("Searching...");
        $scope.layout.items_search_keyword = tag;
        $scope.layout.show_items_search_results = true;
        return $scope.items_search_results = Item.search({
          tags: tag
        });
      };
      infinite_scroll_items = new InfiniteScroll(Item);
      $scope.load_items = function() {
        infinite_scroll_items.config({
          model_types: ["Item"],
          init_starts: $scope.items.length,
          user_id: $scope.user_id
        });
        $scope.layout.loading.items = true;
        $scope.items = infinite_scroll_items.load($scope.items);
        return $scope.items.$asPromise().then(function(response) {
          infinite_scroll_items.success_handler(response);
          return $scope.layout.loading.items = false;
        }, function() {
          return Alert.show_msg("All items are downloaded ...");
        });
      };
      $scope.display_tab = function(tab_name) {
        var profile, tag;
        $scope.layout.display_tab = tab_name;
        if (tab_name === "items") {
          $scope.load_first_items();
        }
        if (tab_name === "settings") {
          profile = $scope.profile;
          $scope.primary_area = profile.primary_area;
          $scope.interested_areas_array = profile.interested_areas.split(",");
          return $scope.interested_areas_tags = [
            (function() {
              var _i, _len, _ref, _results;
              _ref = $scope.interested_areas_array;
              _results = [];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                tag = _ref[_i];
                _results.push({
                  text: tag
                });
              }
              return _results;
            })()
          ][0];
        }
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
        item.owner = Auth.get_profile().id;
        item.is_new = true;
        $scope.items.splice(0, 0, item);
        $("html, body").animate({
          scrollTop: $("#items-display").offset().top - 100
        });
        return true;
      };
      return $scope.change_profile_photo = function() {
        return Album.get_albums().then(function(response) {
          $scope.profile.social_account_photo = response;
          return $scope.profile.$save();
        });
      };
    }
  ]);

}).call(this);
