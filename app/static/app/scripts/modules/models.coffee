'user strict'

angular.module 'worldsheet.models', [
  'restmod'
]
.config (restmodProvider) ->
  restmodProvider.rebase $config:
    primaryKey: "id"
    style: "ams"
    urlPrefix: "/app/"

.factory "Handlers", ["settings", (settings)->
  return{
    handler: (container, base_handler)->
      if Array.isArray(container)
        for record in container
          base_handler(record)
      else
        base_handler(container)
    images_base_handler: (record)->
      if record.images?
        for image in record.images
          if not (/^http/.test(image.url))
            url = image.url
            url_abs = "#{settings.UPLOADED_URL}#{url}"
            console.log "url_abs", url_abs
            image.url = url_abs

    tags_base_handler: (record)->
      if record.tags?
        if typeof(record.tags) == "string"
          if record.tags.length > 0
            record.tags = record.tags.split(",")
            record.tags_input = [{"text": tag} for tag in record.tags][0]
          else
            record.tags = []
            record.tags_input = []
      if record.tags_private?
        if typeof(record.tags_private) == "string"
          if record.tags_private.length > 0
            record.tags_private = record.tags_private.split(",")
            record.tags_private_input = [
              {"text": tag} for tag in record.tags_private
            ][0]
          else
            record.tags_private = []
            record.tags_private_input = []

    images_handler: (container)->
      @handler(container, @images_base_handler)
    tags_handler: (container)->
      @handler(container, @tags_base_handler)
  }
]


.factory "Model", ['restmod', "Alert", "Handlers", (restmod, Alert, Handlers) ->

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
          "after-feed": ()->
            if this.tags_handler?
              this.tags_handler()
            if this.images_handler?
              this.images_handler()
            if this.post_search_handler?
              this.post_search_handler()
          "after-save": ()->
            if self.tags_handler?
              self.tags_handler()
            if self.images_handler?
              self.images_handler()
        $extend:
          Record:
            loading: false
            is_valid: ()->
              return true
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
              Handlers.tags_handler(this)
            fetch: (params)->
              self = this
              this.loading = true
              this.$fetch(params).$then (response)->
                console.log "fetch"
                if response.tags_handler?
                  response.tags_handler()
                if response.images_handler?
                  response.images_handler()
          Collection:
            path: path
            loading: false
            page: 1
            start: 0
            num_of_records: 8
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
                if record.tags_handler?
                  record.tags_handler()
            images_handler: ()->
              for record in this
                if record.images_handler?
                  record.images_handler()
          Model:
            transform: (obj) ->
              record = this.$build(this.init)
              return record.copy(obj)
            search: (params)->
              this.loading = true
              this.$search(params)
      )
  }
]

.factory 'Post', ["Model", "Item", "Auth", (Model, Item, Auth) ->

  condition_choices = ["New", "Like new", "Good", "Functional", "Broken"]

  init = {
    title: ""
    area: ""
    detail: ""
    items: []
    is_new: true
    visibility: "Public"
  }

  # Record method
  add_item = (self) ->
    if 'items' of self
      item = Item.$build(Item.init)
      item.owner = Auth.get_user().id
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
              # Set all attached items (that belong to the post owner)
              # to be public visible

              # Handle the tags of the items
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


.factory "Item",
  ["Model", "settings", "Handlers", "Image",
  (Model, settings, Handlers, Image) ->

    condition_choices = ["Inapplicable", "New", "Like new", "Good", "Functional", "Broken"]
    visibility_choices = ["Public", "Private", "Ex-owners"]
    availability_choices = ["Available", "In use", "Lent", "Given away", "Disposed"]
    utilization_choices = ["Inapplicable", "Daily", "Frequent", "Sometimes", "Rarely", "Never"]

    # Turn "CustomizedCharField" into "customized_char_fields", etc.
    customized_fields_normalization = (self, field)->
      model = field.model_name.toLowerCase()
      model = model.replace("customized", "customized_")
      model = model.replace("field", "_fields")
      return {
        model_name: model
        title: field.title
      }

    customized_fields = ["customized_#{type}_fields" for type in ['char', 'num', 'color', 'date', 'email']][0]

    # For brand new and existing items to be edited
    init = {
      title: ""
      quantity: 1
      condition: "Good"
      utilization: "Sometimes"
      visibility: "Private"
      available: "No"
      status: ""
      new_status: ""
      expanded: false
      is_new: false
    }

    customized_fields_cleaner = (field_type, field_handler)->
      # If the type of fields does not exist or is empty
      if not self[field_type]?
        return
      if not self[field_type]
        return
      fields = self[field_type]
      for field in fields
        # Remove empty (empty title or value) customized fields
        if not (field.value and field.title)
          index = fields.indexOf(field)
          self.customized_num_fields.splice index, 1
        else
          # User can further specify a function to take care
          # of the fields if title and value are present
          if field_handler?
            field_handler(field)

    is_valid = (self)->
      if not self.title
        false
      true

    return Model.create("/items/").mix({
      $hooks:
        'after-save': ()->
          this.tags_handler()
          this.images_handler()
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
            # In [transfer-menu] directive
            # transferring will attach a new_owner property
            if "new_owner" of self
              if self["new_owner"]
                self.owner = self['new_owner'].id
            # if the self.tags is in array type,
            # merge them into string.
            if self.new_status
              self.status = self.new_status
            # Tags handlers
            if "tags" of self
              if typeof(self.tags) == "object"
                self.tags = self.tags.join(",")
            if "tags_private" of self
              if typeof(self.tags_private) == "object"
                self.tags_private = self.tags_private.join(",")
            # Clean up customized fields
            # - Remove empties
            for field in customized_fields
              customized_fields_cleaner(
                field,
              )
            # further processing of valid fields
            customized_fields_cleaner(
              "customized_num_fields",
              (field)->
                field.value = parseFloat(field.value)
            )

          images_handler: ()->
            Handlers.images_handler(this)
            length = this.images.length
            for i in [0...length]
              image = this.images[i]
              this.images[i] = Image.transform(image)
          tags_handler: ()->
            Handlers.tags_handler(this)
          add_customized_field: (type)->
            self = this
            field_type = "customized_#{type}_fields"
            if not self[field_type]?
              self[field_type] = []
            init_val = {
              title: ""
              value: ""
            }
            if type == 'num'
              init_val['unit'] = ""
            self[field_type].push(init_val)
        Collection:
          tags_handler: ()->
            for record in this
              Handlers.tags_handler(record)
        Model:
          init: init
          customized_fields_normalization: (field)->
            customized_fields_normalization(this, field)
          customized_fields: customized_fields
    })
]

.factory "BulkItems", ["Model", (Model)->
  return Model.create("/bulk-items/")
]

.factory "Feed", ["Model", (Model) ->
  return Model.create("/feeds/").mix(
    $extend:
      record:""
  )
]

.factory "Timeline", ["Model", (Model) ->
  # For current user's dashboard timeline
  return Model.create("/timeline/")
]

.factory "ItemTimeline", ["Model", (Model) ->
  # for the timeline of an item
  return Model.create("/timeline/item/")
]

.factory "UserTimeline", ["Model", (Model) ->
  # for the timeline of a specific user
  return Model.create("/timeline/user/")
]

.factory "Transaction", ["Model", (Model)->
  return Model.create("/transactions/").mix(
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

.factory "Update", ["Model", (Model)->

  return Model.create("/updates/")

]

.factory "InfiniteScroll", ["settings", "Handlers", (settings, Handlers)->

  return class InfiniteScroll
    model_types: []    # The expected model_types returned from the backend
    init_starts: undefined
    monitor: 0
    constructor: (Model)->
      @Model = Model     # The restmod model that calls search() or fetch()
    config: (configs)=>
      for cf of configs
        @[cf] = configs[cf]
    tags_handler: (container)->
      # parent is the object that might contain
      # <tags> attribute
      if container.tags?
        if container.tags_handler?
          container.tags_handler()
        else
          Handlers.tags_handler(container)
    images_handler: (container)->
      # container is the object that might contain
      # <images> attribute
      if container.images?
        if container.images_handler?
          container.images_handler()
        else
          Handlers.images_handler(container)
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
        if response.images_handler?
          response.images_handler()

      else if @model_types.length > 1
        response.starts = {}
        for model_name of @init_starts
          response.starts[model_name] = @init_starts[model_name]
        for record in response
          model_name = record.model_name
          response.starts[model_name] += 1
          if record.items?    # Typically for post
            if record.items.length
              for item in record.items
                @tags_handler(item)
                @images_handler(item)
          if record.item?     # Typically for transaction and updates
            @tags_handler(record.item)
            @images_handler(record.item)
      return response

]

.factory "Image", ["Model", (Model) ->
  return Model.create("/images/").mix(
    $extend:
      Record:
        delete: ()->
          this.$destroy().$then ()->
            console.log "delete"
  )
]

.factory "Profile", ["Model", (Model) ->
  return Model.create("/profiles/").mix(
    $extend:
      Record:
        pre_save_handler: ()->
          self = this
          self.accept_donations_categories = ''
          if self.tags_accept_donations_categories
            categories = [tag.text for tag in self.tags_accept_donations_categories]
            self.accept_donations_categories = categories.join(",")
        tags_handler: ()->
          self = this
          self.tags_accept_donations_categories = []
          if self.accept_donations_categories
            self.tags_accept_donations_categories = [{text: tag} for tag in self.accept_donations_categories.split(",")][0]
        is_valid: ()->
          true
        post_search_handler: ()->
          if not this.ordering_fields
            this.ordering_fields = []
      Collection:
        post_search_handler: ()->
          for record in this
            if record.post_search_handler?
              record.post_search_handler()
  )
]

.factory "Auth", ["Profile", "Alert", (Profile, Alert)->
  profile = {}
  return{
    fetch_profile: () ->
      Profile.search().$asPromise()
    store_profile: (response)->
      profile = response
    get_profile: ()->
      profile
  }
]


.factory "Attendant", ["Model", (Model)->

  return Model.create("/attendants/").mix(
    $extend:
      Model:
        statistics: (activity, date)->
          if not date?
            date = null
          this.search(
            statistics:true
            activity: activity
            date: date
          )
        fields: ()->
          this.search(
            fields: true
          )
  )

]