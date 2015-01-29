angular.module "continue"

.controller "postEditorCtrl", [
  "$scope", "Post", "ItemSelector", "ItemEditor", "Alert", "$upload", "Auth", "settings",
  ($scope, Post, ItemSelector, ItemEditor, Alert, $upload, Auth, settings)->
    $scope.new_items = []
    $scope.images_list = []
    $scope.test_image = "http://localhost:8000/static/uploaded/item_images/ipad_4UnR7b1.jpg  
"
    $scope.post = Post.$build(Post.init)
    $scope.layout = {
      detail_input: false
    }
    $scope.submission_error = false
    # If 'id' is specified, load the post from server.
    $scope.$watch "id", ()->
      if $scope.id?
        $scope.post = Post.$find($scope.id)
        $scope.post.$then (response)->
          this.tags_handler()
          $('textarea').val(this.detail).trigger('autosize.resize')
          if this.tags.length > 0
            $scope.tags_input = [{"text": tag} for tag in this.tags][0]
          if this.images
            images_url_list = this.images.split(",")
            $scope.images_list = [{
              url: url
              markdown: "![](#{url})"
            } for url in images_url_list][0]

    $scope.$watch "images", ()->
      if $scope.images
        $scope.upload = $upload.upload(
          url: "/app/images/"
          data:
            owner: Auth.get_profile().id
          file: $scope.images
        ).progress((evt) ->
          console.log "progress: " + parseInt(100.0 * evt.loaded / evt.total) + "% file :" + evt.config.file.name
          return
        ).then (response)->
          console.log response
          url_rel = response.data.url
          url = "#{settings.UPLOADED_URL}#{url_rel}"
          post = $scope.post
          img = {
            url: url
            markdown: "![](#{url})"
          }
          $scope.images_list.push(img)
          $scope.images = undefined
        , ()->
          Alert.show_error("There was problem uploading your file. Please make sure your file is a valid image file.")

    $scope.show_detail_editor = ()->
      $scope.layout.detail_input = true
      $("textarea").resize()
      return true

    $scope.select_item = ()->
      Alert.show_msg("Loading your items ...")
      # $scope.post.items is passed in as existed items,
      # used to remove duplicated items from the BottomSheet.
      ItemSelector.begin($scope.post.items).then (response)->
        if response
          $scope.post.items.push(response)
          $scope.new_items.push(response)

    $scope.add_new_item = ()->
      ItemEditor.begin().then (response)->
        console.log "haha2 in add_new_item"
        if response
          $scope.post.items.push(response)
          $scope.new_items.push(response)


    $scope.reset = ()->
      $scope.post.$fetch()
      $scope.new_items = []

    $scope.save = ()->
      if not $scope.postEditor.$valid
        $scope.submission_error = true
        Alert.show_error("You input maybe incomplete, or invalid.")
        return
      if $scope.post.visibility == "Invitation" and not $scope.post.secret_key
        $scope.missing_key = true
      if $scope.images_list.length
        images = [img.url for img in $scope.images_list].join(",")
        $scope.post.images = images
      if $scope.tags_input.length
        tags_array = [tag.text for tag in $scope.tags_input]
        tags = tags_array.join(",")
        $scope.post.tags = tags
      $scope.post.owner = Auth.get_profile().id
      $scope.post.save().$then (response)->
        if "id" of response
          return
          # window.location.replace("/app/post/#{response.id}/")
      , (e)->
        console.log e

]