angular.module("worldsheet")
.controller "EditCtrl",  ["$scope", "$location", "get_item", ($scope, $location, get_item)->
  $scope.item = get_item
  $scope.expand = ()->
    console.log "haha"
]

.directive "itemEditorLite", [
  "Alert", "Item", "Album", "Auth", "$upload", "settings", "$modal",
  (Alert, Item, Album, Auth, $upload, settings, $modal)->
    restrict: "E"
    templateUrl: "/static/app/scripts/components/item-editor/item-editor-lite.html"
    scope:
      item: "=item"
    link: (scope)->
      scope.customized_fields = Item.customized_fields

      scope.show_more = false
      $('textarea').autosize()

      scope.open_modal = (item)->
        console.log "haha"
        modal = $modal.open(
          templateUrl: "/static/app/scripts/components/item-editor/modal.html"
          size: 'lg'
          controller: 'EditCtrl'
          backdropClass: "modal-backdrop"
          resolve:
            get_item: ()->
              return item
        )

      scope.layout = {
        uploading: false
        upload_progress: 0
      }

      scope.$watch "files", ()->
        if scope.files
          scope.uploading = true
          scope.upload = $upload.upload(
            url: "/app/images/"
            data:
              owner: Auth.get_profile().id
            file: scope.files
          ).progress((evt) ->
            console.log "progress: " + parseInt(100.0 * evt.loaded / evt.total) + "% file :" + evt.config.file.name
            scope.layout.upload_progress = parseInt(100.0 * evt.loaded / evt.total)
            return
          ).then (response)->
            console.log "response = ", response
            url_rel = response.data.url
            url_abs = "#{settings.UPLOADED_URL}#{url_rel}"
            item = scope.item
            if not item.pic
              item.pic = url_abs
            item.images.push(response.data)
            scope.save(item)
            scope.layout.uploading = false
          , ()->
            scope.layout.uploading = false
            Alert.show_error("There was problem uploading your file. Please make sure your file is a valid image file.")

      scope.save = (item)->
        success_handler = (item)->
          item.expanded = false
          item.new_status = ""
          item.is_new = false
        tags = [tag.text for tag in item.tags_input][0].join(",")
        tags_private = [tag.text for tag in item.tags_private_input][0].join(",")
        item.tags = tags
        item.tags_private = tags_private
        console.log "saving"
        item.save(success_handler).$asPromise()

      scope.expand = (item) ->
        console.log "expand"
        if item.expanded isnt true
          console.log "expand"
          item.expanded = true
        else
          console.log "fold"
          item.expanded = false
        return
]

.directive "itemEditorPro", [
  "Alert", "Album", "Auth", "$upload", "settings"
  (Alert, Album, Auth, $upload, settings)->
    restrict: "E"
    templateUrl: "/static/app/scripts/components/item-editor/item-editor-pro.html"
    scope:
      item: "=item"
    link: (scope)->

      scope.show_more = false
      $('textarea').autosize()


      scope.layout = {
        uploading: false
        upload_progress: 0
      }

      scope.$watch "files", ()->
        if scope.files
          scope.uploading = true
          scope.upload = $upload.upload(
            url: "/app/images/"
            data:
              owner: Auth.get_profile().id
            file: scope.files
          ).progress((evt) ->
            console.log "progress: " + parseInt(100.0 * evt.loaded / evt.total) + "% file :" + evt.config.file.name
            scope.layout.upload_progress = parseInt(100.0 * evt.loaded / evt.total)
            return
          ).then (response)->
            console.log "response = ", response
            url_rel = response.data.url
            url_abs = "#{settings.UPLOADED_URL}#{url_rel}"
            item = scope.item
            if not item.pic
              item.pic = url_abs
            item.images.push(response.data)
            scope.save(item)
            scope.layout.uploading = false
          , ()->
            scope.layout.uploading = false
            Alert.show_error("There was problem uploading your file. Please make sure your file is a valid image file.")

      scope.save = (item)->
        success_handler = (item)->
          item.expanded = false
          item.new_status = ""
          item.is_new = false
        tags = [tag.text for tag in item.tags_input][0].join(",")
        tags_private = [tag.text for tag in item.tags_private_input][0].join(",")
        item.tags = tags
        item.tags_private = tags_private
        item.save(success_handler).$asPromise()

      scope.expand = (item) ->
        if item.expanded isnt true
          console.log "expand"
          item.expanded = true
        else
          console.log "fold"
          item.expanded = false
        return
]

.directive "itemEditorTitle", ()->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/item-editor-pro-title.html"

.directive "itemEditorBasics", ["Album", "Alert", (Album, Alert)->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/item-editor-pro-basics.html"
  link: (scope)->
    scope.get_albums = (item)->
      Alert.show_msg("Downloading your albums ...")
      Album.get_albums().then (response)->
        if response
          item.pic = response
          item.save()

]

.directive "itemEditorLiteMore", ["Auth", (Auth)->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/item-editor-lite-more.html"
]

.directive "itemEditorProMore", ["Auth", (Auth)->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/item-editor-pro-more.html"
  link: (scope)->

    scope.set_as_ordering = (field)->
      profile = Auth.get_profile()
      ordering_fields = profile.ordering_fields
      new_ordering_field = {"title": field.title, "model_name": field.model_name}
      if not _.find(ordering_fields, new_ordering_field)
        ordering_fields.push(new_ordering_field)
      profile.save()

    
    scope.open = ($event) ->
      $event.preventDefault()
      $event.stopPropagation()
      scope.datepicker_opened = true
]

.directive "itemFieldEditMenu", ()->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/item-field-edit-menu.html"

.directive "customizedFieldTitle", ()->
  restrict: "E"
  templateUrl: "/static/app/scripts/components/item-editor/customized-field-title.html"
  link:(scope, element, attrs)->
    console.log "customizedFieldTitle"