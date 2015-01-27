angular.module "continue"

.factory "BS", ["$q", ($q) ->

  # Register templateUrls for each service that will use BS
  templateUrls = {
    "item-detail": "/static/app/directives/dashboard-item-overview.html"
    "album": "/static/app/scripts/services/album/album.html"
    "private-message": "/static/app/scripts/services/private-message/private-message.html"
    "item-editor": "/static/app/directives/item-editor.html"
    "item-selector": "/static/app/directives/item-selector.html"
  }

  return {
    contentUrl: ""
    monitor: 0
    promise: undefined
    deferred: undefined   # waiting to be resolved and close the BottomSheet.
    output: undefined
    input: undefined
    bringUp: (content_type)->
      """
      Return a <deferred object>. Other services can call BS.bringUp()
      and resolve it when appropriate.
      BS do not store content data for the bottom-sheet. All data
      should be provided by the calling service, and controller 
      that control the content, specified by the <content_type>
      """
      self = this
      self.is_show = true
      self.contentUrl = templateUrls[content_type]
      # Setting up for closing the Bottom sheet
      deferred = $q.defer()
      deferred.promise.then ()->
        self.is_show = false
      self.promise = deferred.promise
      self.deferred = deferred
      self.monitor += 1
      return deferred

    close: ()->
      this.is_show = false
      this.deferred.resolve()
      this.deferred.promise
  }
]

.directive "bS", ["BS", (BS)->
  restrict: "E"
  templateUrl: "/static/app/scripts/services/BS/BS.html"
  link: (scope, element, attrs)->
    scope.BS = BS
    scope.$watch "BS.monitor", ()->
      scope.contentUrl = BS.contentUrl
]



.factory "ItemEditor", ["Item", "BS", "Auth", (Item, BS, Auth)->
  return{
    item: {}
    monitor: 0
    deferred: {}
    refresh: false
    begin: (input, refresh)->
      # input might be item_id, namely of <string> type
      # might be an item object
      self = this
      if refresh?
        self.refresh = refresh
      if input?
        # if only supply an id, download the item
        if typeof(input) == "string"
          self.item = Item.$find(input)
          self.item.$then (response)->
            console.log "self.item.tags_handler"
            self.item.tags_handler()
            self.deferred = BS.bringUp("item-editor")
            self.monitor += 1
            console.log "self.deferred.promise", self.deferred.promise
            return self.deferred.promise
          .$asPromise()   # the restmod $then must explicitly use .$asPromise()
                          # to forward any promise object inside the $then()
        else if typeof(input) == "object"
          self.item = input
          self.item.is_new = true
          # the item should be Public
          # since the bottom sheet is called in post editor
          self.item.visibility = "Public"
          # Copy the deferred object from the BottomSheet
          self.deferred = BS.bringUp("item-editor")
          self.monitor += 1
          console.log "self.deferred.promise", self.deferred.promise
          return self.deferred.promise
      else    # create brand new item
        self.item = Item.$build(Item.init)
        self.item.is_new = true
        self.item.owner = Auth.get_profile().user_id
        # the item should be Public
        # since the bottom sheet is called in post editor
        self.item.visibility = "Public"
        self.deferred = BS.bringUp("item-editor")
        self.monitor += 1
        return self.deferred.promise
  }
]

.directive "itemEditor", ["ItemEditor", (ItemEditor)->
  restrict: "AE"
  link: (scope, element, attrs)->
    scope.ItemEditor = ItemEditor
    scope.$watch "ItemEditor.monitor", ()->
      scope.item = ItemEditor.item
    scope.add_to_post = ()->
      ItemEditor.deferred.resolve(scope.item)
      ItemEditor.item = {}
      scope.item = {}
    scope.update_item = (item)->
      # resolve the previous Item.$find(), otherwise
      # it will not run the new save() request.
      ItemEditor.deferred.resolve(item)
      item.save().$then (response)->
        scope.item = {}
]

.factory "ItemSelector", ["Item", "BS", (Item, BS)->
  return{
    items: []
    deferred: {}
    monitor: 0
    existed_items: {}
    begin: (existed_items)->
      self = this
      self.existed_items = existed_items
      self.items = Item.$search(
        page:1
        num_of_records: 8
      )
      self.items.$asPromise().then (response)->
        console.log "ItemSelector tags_handler()"
        self.items.tags_handler()
        self.deferred = BS.bringUp("item-selector")
        self.monitor += 1
        console.log "self.items ========>", self.items
        self.deferred.promise
  }
]

.directive "itemSelector", ["ItemSelector", (ItemSelector)->
  restrict: "AE"
  link: (scope)->
    scope.ItemSelector = ItemSelector
    scope.select = (item)->
      ItemSelector.deferred.resolve(item)
    scope.$watch "ItemSelector.monitor", ()->
      scope.items = ItemSelector.items
      scope.existed_items = ItemSelector.existed_items
      scope.items.num_of_records = 8
    
    scope.duplicated = (item)->
      duplicated = false
      for existed in scope.existed_items
        if item.id == existed.id
          duplicated = true
      return duplicated
]
