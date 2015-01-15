angular.module "continue"

.factory "Album", ["$q", "FB", "Auth", "BS", ($q, FB, Auth, BS)->
  get_photos = (self, album_id)->
    self.album = album_id
    FB.resource.get(
      node: album_id
      edge: "photos"
      access_token: Auth.get_user().social_account_access_token
      fields: "images"
    )
    .$promise

  return {
    albums: []
    photos: []
    photo: ""
    is_show: false
    deferred: {}
    get_albums: ()->
      self = this
      FB.resource.get(
        node: "me"
        access_token: Auth.get_user().social_account_access_token
        fields: "id, albums{cover_photo}"
      )
      .$promise
      .then (response) ->
        # The response should be information about the user
        # and an array of albums
        self.albums = response.albums.data
        album_covers = []
        for album in self.albums
          album_covers.push(album.cover_photo)
        ids = album_covers.toString()
        # Using ids, one can perform multiple request to Graph API
        covers = FB.resource.get(
          access_token: Auth.get_user().social_account_access_token
          ids: ids
          fields: "images"
        )
        return covers.$promise
      .then (response)->
        # Store all cover photos data into self.albums
        index = 0
        for cover_photo of response
          if index < self.albums.length
            self.albums[index].cover_photo = response[cover_photo]
          index += 1
        console.log self.albums
        console.log "all cover photos are obtained."

        self.deferred = BS.bringUp("album")
        self.deferred.promise


    get_photos: (album_id)->
      get_photos(this, album_id)

  }
]

.controller "albumCtrl", ["$scope", "Album", ($scope, Album)->
  $scope.layout = {
    album_list_is_show: true
    page: 1
    num_of_records: 8
  }
  $scope.Album = Album

  $scope.photos_to_display = ()->
    start = ($scope.layout.page - 1) * $scope.layout.num_of_records
    end = Math.min($scope.layout.page * $scope.layout.num_of_records, Album.photos.length - 1)
    Album.photos[start..end]

  $scope.pagination = (array)->
    start = ($scope.layout.page - 1) * $scope.layout.num_of_records
    end = Math.min($scope.layout.page * $scope.layout.num_of_records - 1, array.length - 1)
    array[start..end]

  $scope.back_to_albums = ()->
    $scope.layout.album_list_is_show = true

  $scope.next_page = ()->
    if $scope.layout.album_list_is_show
      array = Album.albums
    else
      array = Album.photos
    if $scope.layout.page * $scope.layout.num_of_records < array.length
      $scope.layout.page += 1

  $scope.prev_page = ()->
    if $scope.layout.page > 1
      $scope.layout.page -= 1

  $scope.select_album = (album_id)->
    Album.get_photos(album_id).then (response)->
      Album.photos = response.data
      $scope.layout.album_list_is_show = false

  $scope.select_photo = (photo)->
    Album.photo = photo.images[2].source
    console.log Album.deferred
    Album.deferred.resolve(Album.photo)
]
