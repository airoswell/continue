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
    deferred: undefined
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



.factory "ItemEditor", ["Item", "BS", (Item, BS)->
  return{
    item: {}
    monitor: 0
    deferred: {}
    begin: (input)->
      self = this
      if input?
        if typeof(input) == "string"
          self.item = Item.$find(input).$then (response)->
            self.deferred = BS.bringUp("item-editor")
            self.monitor += 1
            self.deferred.promise
        else if typeof(input) == "object"
          self.item = input
          self.item.is_new = true
          # the item should be Public
          # since the bottom sheet is called in post editor
          self.item.visibility = "Public"
          self.deferred = BS.bringUp("item-editor")
          self.monitor += 1
          self.deferred.promise
      else
        self.item = Item.$build(Item.init)
        self.item.is_new = true
        # the item should be Public
        # since the bottom sheet is called in post editor
        self.item.visibility = "Public"
        self.deferred = BS.bringUp("item-editor")
        self.monitor += 1
        self.deferred.promise
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
        items_per_page: 8
      )
      self.items.$asPromise().then (response)->
        self.deferred = BS.bringUp("item-selector")
        for item in self.items
          item.duplicated = false
          for existed in existed_items
            if item.id == existed.id
              item.duplicated = true
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
      scope.items.items_per_page = 8
]

.directive "itemTitle", ()->
  restrct: "E"
  scope:
    item: "="
  templateUrl: "/static/app/directives/item-title.html"
  link: (scope, element, attrs)->
    console.log "itemTitle"