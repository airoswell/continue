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
      Alert.show_error("Your input is not complete or contains invalid data.")
      return false
    # Save the record
    self.loading = true
    # By default, saving the object should be under the current user's
    # name
    if self.pre_save_handler?
      self.pre_save_handler()
    Alert.show_msg("Saving your data to database ...")
    self.$save().$then (response) ->
      if self.tags_handler?
        self.tags_handler()
      if successHandler?
        successHandler(self, response)
      Alert.show_msg("Your data is saved! You may need to refresh ...")
      self.loading = false
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
        $hooks:
          "before-request": (_req)->
            _req.url += "/"
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
              if this.tags?
                if typeof(this.tags) == "string"
                  if this.tags
                    this.tags = this.tags.split(",")
                  else
                    this.tags = []
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
              this.$fetch(params).$then (response)->
                if response.tags_handler?
                  response.tags_handler()
            tags_handler: ()->
              for record in this
                record.tags_handler()
          Model:
            transform: (obj) ->
              record = this.$build(this.init)
              return record.copy(obj)
            search: (params)->
              this.loading = true
              this.$search(params).$then (response)->
                if response.tags_handler?
                  response.tags_handler()
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
    if self.visibility == "Invitation" and not self.secret_key
      return false
    return true

  # <Post, Model> method
  search = (self, params) ->
    posts = self.$search(params)
    $then = posts.$then (response) ->
      for post in posts
        if "tags" of post
          if typeof(post.tags) == "string"
            if post.tags
              post.tags = post.tags.split(",")
            else
              post.tags = []
        for i in [0...post.items.length]
          # Originally the item is a plain JSON object
          # transform it into a resource instance,
          # With all possible mod-choices
          item = post.items[i]
          post.items[i] = Item.transform(item)
          if item.tags?
            if typeof(item.tags) == "string"
              if item.tags
                item.tags = item.tags.split(",")
              else
                item.tags = []
          
  visibility_choices = ["Private", "Public", "Invitation"]

  return Model.create('/posts/').mix({
    $extend:
      Record:
        visibility_choices: visibility_choices
        add_item: () ->
          add_item(this)
        is_valid: () ->
          is_valid(this)
        initialize: () ->
          initialize(this)
        pre_save_handler: ()->
          self = this
          if self.visibility != "Invitation"
            self.secret_key = ""
          # Deal with the tags of the post
          if "tags" of self
            if typeof(self.tags) == "object"
              self.tags = self.tags.join(",")
          # Deal with the tags of the items
          if self.items?
            for item in self.items
              if item.tags?
                if typeof(item.tags) == "object"
                  item.tags = item.tags.join(",")
              if item.tags_private?
                if typeof(item.tags_private) == "object"
                  item.tags_private = item.tags_private.join(",")
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
          self = this
          # But if the owner choose a new owner, use the new owner.
          if "new_owner" of self
            if self["new_owner"]
              self.owner = self['new_owner'].id
              self.visibility = "Ex-owners"
          # if the self.tags is in array type,
          # merge them into string.
          if self.new_status
            self.status = self.new_status
          if "tags" of self
            if typeof(self.tags) == "object"
              self.tags = self.tags.join(",")
          if "tags_private" of self
            if typeof(self.tags_private) == "object"
              self.tags_private = self.tags_private.join(",")
        tags_handler: ()->
          if "tags" of this
            if not this.tags
              this.tags = []
              this.tags_input = []
            if typeof(this.tags) == "string"
              if this.tags
                this.tags = this.tags.split(",")
                this.tags_input = [{"text": tag} for tag in this.tags][0]
          if "tags_private" of this
            if not this.tags_private
              this.tags_private = []
              this.tags_private_input = []
            if typeof(this.tags_private) == "string"
              if this.tags_private
                this.tags_private = this.tags_private.split(",")
                this.tags_private_input = [
                  {"text": tag} for tag in this.tags_private
                ][0]
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
          this.save().$then ()->
            location.reload()
        dismiss: ()->
          this.status = "Dismissed"
          this.save().$then ()->
            location.reload()
        receive: ()->
          this.status = "Received"
          this.save().$then ()->
            location.reload()
  )
]

.factory "InfiniteScroll", ()->

  return class InfiniteScroll
    model_types: []    # The expected model_types returned from the backend
    init_starts: undefined
    monitor: 0
    constructor: (Model)->
      @Model = Model     # The restmod model that calls search() or fetch()
    config: (configs)=>
      for cf of configs
        @[cf] = configs[cf]
    base_tags_handler: (parent)->
      if parent.tags?
        if parent.tags_handler?
          parent.tags_handler()
        else
          if typeof(parent.tags) == "string" and parent.tags.length > 0
            parent.tags = parent.tags.split(",")
          else
            parent.tags = []
    params: (model)=>
      if not model?    # if model does not exist, start the first search
        if @model_types.length > 1
          params = {starts: @init_starts}
        else
          params = {start: @init_starts}
      else
        if @model_types.length > 1
          params = starts: model.starts
        else
          params = {start: model.start}
      if @extra_params?
        for key of @extra_params
          params[key] = @extra_params[key] or ""
      return params
    load: (model) =>
      params = @params(model)
      if not model?    # if model does not exist, start the first search
        return @Model.search(params)
      else
        return model.fetch(params)

    success_handler: (response)=>
      if @model_types.length == 1
        response.start = parseInt(@init_starts) + response.length
        if response.tags_handler?
          response.tags_handler()

      else if @model_types.length > 1
        response.starts = {}

        for model_name of @init_starts
          response.starts[model_name] = @init_starts[model_name]

        for record in response
          model_name = record.model_name
          response.starts[model_name] += 1
          if record.items?
            if record.items
              for item in record.items
                @base_tags_handler(item)
      return response


.factory "Image", ["Model", (Model) ->
  return Model.create("/images/").mix(
    $extend:
      record:""
  )
]