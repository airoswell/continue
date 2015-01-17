'user strict'

angular.module 'continue.models', [
  'restmod'
  'continue.auth'
]
.config (restmodProvider) ->
  restmodProvider.rebase $config:
    primaryKey: "id"
    style: "ams"
    urlPrefix: "/app/"

.factory "Model", ['restmod', "Alert", "Auth", (restmod, Alert, Auth) ->

  save = (self, successHandler, errorHandler) ->
    # Prepare for saving
    if not self.is_valid()
      Alert.show_error("Your input contains invalid data.")
      return false
    # Save the record
    self.loading = true
    # By default, saving the object should be under the current user's
    # name
    if "pre_save_handler" of self
      self.pre_save_handler()
    Alert.show_msg("Saving your data to database ...")
    self.$save().$then (response) ->
      Alert.show_msg("Your data is saved! You may need to refresh ...")
      self.loading = false
      if successHandler?
        successHandler(self, response)
    , (errors) ->
      self.loading = false
      Alert.show_error("There are problems processing your data.", 10000)
      if errorHandler?
        errorHandler(self, errors)

  next_page = (self) ->
    Alert.show_msg("Loading ...")

    refresh = self.$refresh(
      page: self.page + 1
      num_of_records: self.num_of_records
    )
    refresh.$asPromise().then (response)->
      self.page += 1
      this.promise
    , (error)->
      Alert.show_msg("That's all the items.")


  prev_page = (self) ->
    Alert.show_msg("Loading ...")
    if self.page > 1
      refresh = self.$refresh(
        page: self.page - 1
        num_of_records: self.num_of_records
      )
      refresh.$then (response) ->
        self.page -= 1

  copy = (self, obj) ->
    """
    Copy properties of <obj> to the record itself.
    """
    if not obj? or typeof obj isnt "object"
      return obj
    for key of obj
      self[key] = obj[key]
    return self

  return {
    create: (path) ->
      restmod.model(path).mix(
        $extend:
          Record:
            loading: false
            save: (successHandler, errorHandler) ->
              save(this, successHandler, errorHandler)
            copy: (obj, property)->
              if not property?
                copy(this, obj)
              else
                if property of obj
                  this[property] = obj[property]
                return this
            tags_handler: ()->
              if "tags" of this
                if typeof(this.tags) == "string"
                  if this.tags
                    this.tags = this.tags.split(",")
          Collection:
            path: path
            loading: false
            page: 1
            start: 0
            num_of_records: 2
            next_page: () ->
              next_page(this)
            prev_page: () ->
              prev_page(this)
            fetch: (params)->
              self = this
              this.loading = true
              this.$fetch(params)
            tags_handler: ()->
              for record in this
                record.tags_handler()
          Model:
            transform: (obj) ->
              record = this.$build(this.init)
              return record.copy(obj)
            search: (params)->
              self.loading = true
              self.$search(params)
      )
  }
]

.factory 'Post', ["$q", "Model", "Item", "Auth", ($q, Model, Item, Auth) ->

  condition_choices = ["New", "Like new", "Good", "Functional", "Broken"]

  init = {
    title: ""
    area: ""
    detail: ""
    items: []
    is_new: true
  }

  # Record method
  add_item = (self) ->
    if 'items' of self
      item = Item.$build(Item.init)
      item.owner = Auth.get_user().user_id
      item.is_new = true
      self['items'].push(item)
      return item

  is_valid = (self) ->
    if not self.title or not self.area
      return false
    for item in self.items
      if item.title.length == 0
        return false
    return true

  # <Post, Model> method
  search = (self, params) ->
    posts = self.$search(params)
    $then = posts.$then (response) ->
      for post in posts
        if "tags" of post
          if typeof(post.tags) == "string"
            post.tags = post.tags.split(",")
        for i in [0...post.items.length]
          # Originally the item is a plain JSON object
          # transform it into a resource instance,
          # With all possible mod-choices
          item = post.items[i]
          post.items[i] = Item.transform(item)
          if "tags" of item
            if typeof(item.tags) == "string"
              item.tags = item.tags.split(",")
          


  return Model.create('/posts/').mix({
    $extend:
      Record: 
        add_item: () ->
          add_item(this)
        is_valid: () ->
          is_valid(this)
        initialize: () ->
          initialize(this)
      Model:
        search: (params)->
          search(this, params)
        init: init
  })
]

.factory "Item", ["Model", (Model) ->

  condition_choices = ["New", "Like new", "Good", "Functional", "Broken"]
  visibility_choices = ["Public", "Private", "Ex-owners"]
  availability_choices = ["Available", "In use", "Lent", "Given away", "Disposed"]
  utilization_choices = ["Frequent", "Sometimes", "Rarely", "Never"]

  # For brand new and existing items to be edited
  init = {
    title: ""
    quantity: 1
    condition: "Good"
    utilization: "Sometimes"
    visibility: "Private"
    availability: "Available"
    status: ""
    new_status: ""
    expanded: false
    is_new: false
  }

  is_valid = (self)->
    if not self.title
      false
    true

  return Model.create("/items/").mix({
    $extend:
      Record:
        condition_choices: condition_choices
        availability_choices: availability_choices
        visibility_choices: visibility_choices
        utilization_choices: utilization_choices
        initialize: ()->
          initialize(this)
        is_valid: () ->
          is_valid(this)
        pre_save_handler: ()->
          console.log "processing data"
          self = this
          # But if the owner choose a new owner, use the new owner.
          if "new_owner" of self
            if self["new_owner"]
              self.owner = self['new_owner'].id
              self.visibility = "Ex-owners"
          # if the self.tags is in array type,
          # merge them into string.
          if "tags" of self
            if typeof(self.tags) == "object"
              self.tags = self.tags.join(",")
      Model:
        init: init
    histories: {hasMany: "History"}
  })
]

.factory "History", ["Model", (Model) ->
  return Model.create("/histories/")
]

.factory "Feed", ["Model", (Model) ->
  return Model.create("/feeds/").mix(
    $extend:
      record:""
  )
]

.factory "Timeline", ["Model", (Model) ->
  return Model.create("/timeline/").mix(
    $extend:
      record:""
  )
]

.factory "Transaction", ["Model", (Model)->
  return Model.create("/transactions/").mix(
    $hooks:
      "before-request": (_req)->
        _req.url += "/"
    $extend:
      Record:
        is_valid: ()->
          true
        pre_save_handler: ()->
          # API expect <pk> value for easy de-serialization
          this.giver = this.giver.id
          this.receiver = this.receiver.id
          this.item = this.item.id
        revoke: ()->
          this.status = "Revoked"
          this.save()
        dismiss: ()->
          this.status = "Dismissed"
          this.save()
        receive: ()->
          this.status = "Received"
          this.save()
  )
]

.factory "InfiniteScroll", ()->

  return{
    model: undefined
    init_starts: undefined
    subsequent_starts: undefined
    monitor: 0
    config: (configs)->
      for cf of configs
        this.cf = configs[cf]
    load: (data_holder)->
      if not data_holder    # if data_holder is empty
        data_holder = model.search(starts: this.init_starts)
      else
        data_holder = model.fetch(starts: this.subsequent_starts)
      return data_holder
    default_tags_handler: (data_holder)->
      for record in data_holder
        # Process the post.tags
        if record.model_name == "Post"
          post = record
          if post.tags
            if typeof(post.tags) == "string"
              post.tags = post.tags.split(",")
          else
            post.tags = []
        if record.model_name == "Item"
          item = record
          if item.tags
            if typeof(item.tags) == "string"
              item.tags = item.tags.split(",")
          else
            item.tags = []
  }