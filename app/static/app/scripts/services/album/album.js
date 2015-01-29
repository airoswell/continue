// Generated by CoffeeScript 1.8.0
(function() {
  angular.module("continue").factory("Album", [
    "$q", "FB", "Auth", "BS", function($q, FB, Auth, BS) {
      var get_photos;
      get_photos = function(self, album_id) {
        self.album = album_id;
        return FB.resource.get({
          node: album_id,
          edge: "photos",
          access_token: Auth.get_profile().access_token,
          fields: "images"
        }).$promise;
      };
      return {
        albums: [],
        photos: [],
        photo: "",
        is_show: false,
        deferred: {},
        get_albums: function() {
          var self;
          self = this;
          if (Auth.get_profile().social_account_provider !== "facebook") {
            self.deferred = BS.bringUp("album");
            return self.deferred.promise;
          }
          return FB.resource.get({
            node: "me",
            access_token: Auth.get_profile().access_token,
            fields: "id, albums{cover_photo}"
          }).$promise.then(function(response) {
            var album, album_covers, covers, ids, _i, _len, _ref;
            self.albums = response.albums.data;
            album_covers = [];
            _ref = self.albums;
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              album = _ref[_i];
              album_covers.push(album.cover_photo);
            }
            ids = album_covers.toString();
            covers = FB.resource.get({
              access_token: Auth.get_profile().access_token,
              ids: ids,
              fields: "images"
            });
            return covers.$promise;
          }).then(function(response) {
            var cover_photo, index;
            index = 0;
            for (cover_photo in response) {
              if (index < self.albums.length) {
                self.albums[index].cover_photo = response[cover_photo];
              }
              index += 1;
            }
            console.log(self.albums);
            console.log("all cover photos are obtained.");
            self.deferred = BS.bringUp("album");
            return self.deferred.promise;
          });
        },
        get_photos: function(album_id) {
          return get_photos(this, album_id);
        }
      };
    }
  ]).controller("albumCtrl", [
    "$scope", "settings", "Album", "Image", "Auth", "Alert", "$upload", function($scope, settings, Album, Image, Auth, Alert, $upload) {
      $scope.layout = {
        album_list_is_show: true,
        page: 1,
        num_of_records: 8,
        method: 'upload'
      };
      $scope.Album = Album;
      $scope.image = "";
      $scope.uploaded = "";
      $scope.$watch("files", function() {
        if ($scope.files) {
          return $scope.upload = $upload.upload({
            url: "/app/images/",
            data: {
              owner: Auth.get_profile().id
            },
            file: $scope.files
          }).progress(function(evt) {
            console.log("progress: " + parseInt(100.0 * evt.loaded / evt.total) + "% file :" + evt.config.file.name);
          }).then(function(response) {
            var url;
            Alert.show_msg("Your image has been uploaded successfully!");
            url = response.data.url;
            $scope.uploaded = "" + settings.UPLOADED_URL + url;
            return Album.deferred.resolve($scope.uploaded);
          }, function() {
            return Alert.show_error("There was problem uploading your file. Please make sure your file is a valid image file.");
          });
        }
      });
      $scope.$watch("image", function() {
        if ($scope.image) {
          Alert.show_msg("Uploading your image ...");
          $scope.image_resource = Image.$build();
          $scope.image_resource.image = $scope.image;
          $scope.image_resource.owner = Auth.get_profile().id;
          return $scope.image_resource.$save().$asPromise().then(function(response) {
            $scope.uploaded = "" + settings.UPLOADED_URL + response.url;
            console.log("$scope.uploaded", $scope.uploaded);
            Alert.show_msg("Your image has been uploaded successfully!");
            return Album.deferred.resolve($scope.uploaded);
          }, function() {
            return Alert.show_error("There was problem uploading your file. Please make sure your file is a valid image file.");
          });
        }
      });
      $scope.photos_to_display = function() {
        var end, start;
        start = ($scope.layout.page - 1) * $scope.layout.num_of_records;
        end = Math.min($scope.layout.page * $scope.layout.num_of_records, Album.photos.length - 1);
        return Album.photos.slice(start, +end + 1 || 9e9);
      };
      $scope.pagination = function(array) {
        var end, start;
        start = ($scope.layout.page - 1) * $scope.layout.num_of_records;
        end = Math.min($scope.layout.page * $scope.layout.num_of_records - 1, array.length - 1);
        return array.slice(start, +end + 1 || 9e9);
      };
      $scope.back_to_albums = function() {
        return $scope.layout.album_list_is_show = true;
      };
      $scope.next_page = function() {
        var array;
        if ($scope.layout.album_list_is_show) {
          array = Album.albums;
        } else {
          array = Album.photos;
        }
        if ($scope.layout.page * $scope.layout.num_of_records < array.length) {
          return $scope.layout.page += 1;
        }
      };
      $scope.prev_page = function() {
        if ($scope.layout.page > 1) {
          return $scope.layout.page -= 1;
        }
      };
      $scope.select_album = function(album_id) {
        return Album.get_photos(album_id).then(function(response) {
          Album.photos = response.data;
          return $scope.layout.album_list_is_show = false;
        });
      };
      $scope.select_photo = function(photo) {
        Album.photo = photo.images[2].source;
        return Album.deferred.resolve(Album.photo);
      };
      $scope.select_uploaded = function() {
        return Album.deferred.resolve($scope.uploaded);
      };
      return $scope.cancel = function() {
        return Album.deferred.resolve();
      };
    }
  ]);

}).call(this);
