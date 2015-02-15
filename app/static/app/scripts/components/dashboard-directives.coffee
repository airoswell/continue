angular.module("continue")

.directive "itemEditorPro", [
  "Alert", "Album", "Auth", "$upload", "settings"
  (Alert, Album, Auth, $upload, settings)->
    restrict: "E"
    templateUrl: "/static/app/directives/item-editor-pro.html"
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

.directive "itemEditorProTitle", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/item-editor-pro-title.html"

.directive "itemEditorProBasics", ["Album", "Alert", (Album, Alert)->
  restrict: "E"
  templateUrl: "/static/app/directives/item-editor-pro-basics.html"
  link: (scope)->
    scope.get_albums = (item)->
      Alert.show_msg("Downloading your albums ...")
      Album.get_albums().then (response)->
        if response
          item.pic = response
          item.save()

]

.directive "itemEditorProMore", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/item-editor-pro-more.html"
  link: (scope)->
    
    scope.open = ($event) ->
      $event.preventDefault()
      $event.stopPropagation()
      scope.datepicker_opened = true

.directive "itemFieldEditMenu", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/item-field-edit-menu.html"

.directive "postOverview", ->
  restrict: "E"
  templateUrl: "/static/app/directives/post-overview.html"

.directive "dashboardItemOverview", ["Album", "Alert", (Album, Alert)->
  restrict: "E"
  scope: true
  templateUrl: "/static/app/directives/dashboard-item-overview.html"
  link: (scope, element, attrs) ->
    
    element.on "click", (e)->
      if "trigger" of e.target.attributes
        scope.expand(scope.item)
        scope.$apply()
]

.directive "angularItemUpdate", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/angular-item-update.html"

.directive "inputText", ->
  restrict: "E"
  templateUrl: "/static/app/directives/input-text.html"
  scope:
    data: "="
    label: "="
    placeHolder: "="
    inputClass: "="
    containerClass: "="

.directive "inputDropdown", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-dropdown.html"
  scope:
    data: "="
    label: "="
    choices: "="
    containerClass: "="
    transfer: "="
    user: "="
  link: (scope, element, attrs) ->
    scope.dropdown = false
    trigger = element.find("[trigger]")
    trigger
    .on("click", () ->
      scope.dropdown = true
      min_width = element.width()
      console.log "min_width", min_width
      trigger.find("[target]").css({"min-width": min_width})
      scope.$apply()
    )
    .on("mouseleave", () ->
      scope.dropdown = false
      scope.$apply()
    )
    scope.select = (option) ->
      scope.data = option

.directive "inputTextarea", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-textfield.html"
  scope:
    data: "="
    label: "="
    containerClass: "@"
    inputClass: "@"
    placeHolder: "="

.directive "inputDate", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-date.html"
  replace: true
  scope:
    date: "="
    label: "@"

.directive "inputNum", ()->
  restrict: "E"
  templateUrl: "/static/app/directives/input-num.html"
  scope:
    num: "="
    label: "@"
  link: (scope, element)->
    scope.click = ()->
      element.find("input").focus()
      true

.directive "donationSettingForm", ()->
  restrict: "A"

.directive "areaSettingForm", ["Auth", "Alert", (Auth, Alert)->
  restrict: "A"
  link: (scope, element, attrs)->

    validate = ()->
      for tag in scope.interested_areas_tags
        if not /^\d{5}$/.test(tag.text)
          return false
      return  true
    scope.submit_areas_setting = ()->
      if not validate()
        Alert.show_error("Zip code can only contain 5 numeric digits.", 2000)
        return
      zip_codes = []
      for tag in scope.interested_areas_tags
        zip_codes.push(tag.text)
      scope.interested_areas = zip_codes.join() 
      console.log scope.interested_areas
      Alert.show_msg("Submitting ...")

      profile = Auth.get_profile()
      profile.primary_area = scope.primary_area
      profile.interested_areas = scope.interested_areas
      profile.already_set = true
      profile.save().$then (response)->
        scope.hide_area_setting = true
        Alert.show_msg("Your data is saved.")
]