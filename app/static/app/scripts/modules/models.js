// Generated by CoffeeScript 1.8.0
(function() {
  'user strict';
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  angular.module('continue.models', ['restmod', 'continue.auth']).config(function(restmodProvider) {
    return restmodProvider.rebase({
      $config: {
        primaryKey: "id",
        style: "ams",
        urlPrefix: "/app/"
      }
    });
  }).factory("Handlers", [
    "settings", function(settings) {
      return {
        handler: function(container, base_handler) {
          var record, _i, _len, _results;
          if (Array.isArray(container)) {
            _results = [];
            for (_i = 0, _len = container.length; _i < _len; _i++) {
              record = container[_i];
              _results.push(base_handler(record));
            }
            return _results;
          } else {
            return base_handler(container);
          }
        },
        images_base_handler: function(record) {
          var image, url, url_abs, _i, _len, _ref, _results;
          if (record.images != null) {
            _ref = record.images;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              image = _ref[_i];
              if (!(/^http/.test(image.url))) {
                url = image.url;
                url_abs = "" + settings.UPLOADED_URL + url;
                _results.push(image.url = url_abs);
              } else {
                _results.push(void 0);
              }
            }
            return _results;
          }
        },
        tags_base_handler: function(record) {
          var tag;
          if (record.tags != null) {
            if (typeof record.tags === "string") {
              if (record.tags.length > 0) {
                record.tags = record.tags.split(",");
                record.tags_input = [
                  (function() {
                    var _i, _len, _ref, _results;
                    _ref = record.tags;
                    _results = [];
                    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                      tag = _ref[_i];
                      _results.push({
                        "text": tag
                      });
                    }
                    return _results;
                  })()
                ][0];
              } else {
                record.tags = [];
                record.tags_input = [];
              }
            }
          }
          if (record.tags_private != null) {
            if (typeof record.tags_private === "string") {
              if (record.tags_private.length > 0) {
                record.tags_private = record.tags_private.split(",");
                return record.tags_private_input = [
                  (function() {
                    var _i, _len, _ref, _results;
                    _ref = record.tags_private;
                    _results = [];
                    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                      tag = _ref[_i];
                      _results.push({
                        "text": tag
                      });
                    }
                    return _results;
                  })()
                ][0];
              } else {
                record.tags_private = [];
                return record.tags_private_input = [];
              }
            }
          }
        },
        images_handler: function(container) {
          return this.handler(container, this.images_base_handler);
        },
        tags_handler: function(container) {
          return this.handler(container, this.tags_base_handler);
        }
      };
    }
  ]).factory("Model", [
    'restmod', "Alert", "Handlers", function(restmod, Alert, Handlers) {
      var copy, next_page, prev_page, save;
      save = function(self, successHandler, errorHandler) {
        if (!self.is_valid()) {
          Alert.show_error("Your input is not complete or contains invalid data.");
          return false;
        }
        self.loading = true;
        if (self.pre_save_handler != null) {
          self.pre_save_handler();
        }
        Alert.show_msg("Saving your data to database ...");
        return self.$save().$then(function(response) {
          if (self.tags_handler != null) {
            self.tags_handler();
          }
          if (self.images_handler != null) {
            self.images_handler();
          }
          if (successHandler != null) {
            successHandler(self, response);
          }
          Alert.show_msg("Your data is saved! You may need to refresh ...");
          return self.loading = false;
        }, function(errors) {
          self.loading = false;
          Alert.show_error("There are problems processing your data.", 10000);
          if (errorHandler != null) {
            return errorHandler(self, errors);
          }
        });
      };
      next_page = function(self) {
        var refresh;
        Alert.show_msg("Loading ...");
        refresh = self.$refresh({
          page: self.page + 1,
          num_of_records: self.num_of_records
        });
        return refresh.$asPromise().then(function(response) {
          self.page += 1;
          return this.promise;
        }, function(error) {
          return Alert.show_msg("That's all the items.");
        });
      };
      prev_page = function(self) {
        var refresh;
        Alert.show_msg("Loading ...");
        if (self.page > 1) {
          refresh = self.$refresh({
            page: self.page - 1,
            num_of_records: self.num_of_records
          });
          return refresh.$then(function(response) {
            return self.page -= 1;
          });
        }
      };
      copy = function(self, obj) {
        "Copy properties of <obj> to the record itself.";
        var key;
        if ((obj == null) || typeof obj !== "object") {
          return obj;
        }
        for (key in obj) {
          self[key] = obj[key];
        }
        return self;
      };
      return {
        create: function(path) {
          return restmod.model(path).mix({
            $hooks: {
              "before-request": function(_req) {
                return _req.url += "/";
              }
            },
            $extend: {
              Record: {
                loading: false,
                save: function(successHandler, errorHandler) {
                  return save(this, successHandler, errorHandler);
                },
                copy: function(obj, property) {
                  if (property == null) {
                    return copy(this, obj);
                  } else {
                    if (property in obj) {
                      this[property] = obj[property];
                    }
                    return this;
                  }
                },
                tags_handler: function() {
                  console.log("A");
                  return Handlers.tags_handler(this);
                },
                fetch: function(params) {
                  var self;
                  self = this;
                  this.loading = true;
                  return this.$fetch(params).$then(function(response) {
                    if (response.tags_handler != null) {
                      return response.tags_handler();
                    }
                  });
                }
              },
              Collection: {
                path: path,
                loading: false,
                page: 1,
                start: 0,
                num_of_records: 8,
                next_page: function() {
                  return next_page(this);
                },
                prev_page: function() {
                  return prev_page(this);
                },
                fetch: function(params) {
                  var self;
                  self = this;
                  this.loading = true;
                  return this.$fetch(params).$then(function(response) {
                    if (response.tags_handler != null) {
                      return response.tags_handler();
                    }
                  });
                },
                tags_handler: function() {
                  var record, _i, _len, _results;
                  _results = [];
                  for (_i = 0, _len = this.length; _i < _len; _i++) {
                    record = this[_i];
                    if (record.tags_handler != null) {
                      _results.push(record.tags_handler());
                    } else {
                      _results.push(void 0);
                    }
                  }
                  return _results;
                },
                images_handler: function() {
                  var record, _i, _len, _results;
                  _results = [];
                  for (_i = 0, _len = this.length; _i < _len; _i++) {
                    record = this[_i];
                    if (record.images_handler != null) {
                      _results.push(record.images_handler());
                    } else {
                      _results.push(void 0);
                    }
                  }
                  return _results;
                }
              },
              Model: {
                transform: function(obj) {
                  var record;
                  record = this.$build(this.init);
                  return record.copy(obj);
                },
                search: function(params) {
                  this.loading = true;
                  return this.$search(params).$then(function(response) {
                    console.log("Model.search");
                    if (response.tags_handler != null) {
                      return response.tags_handler();
                    }
                  });
                }
              }
            }
          });
        }
      };
    }
  ]).factory('Post', [
    "Model", "Item", "Auth", function(Model, Item, Auth) {
      var add_item, condition_choices, init, is_valid, search, visibility_choices;
      condition_choices = ["New", "Like new", "Good", "Functional", "Broken"];
      init = {
        title: "",
        area: "",
        detail: "",
        items: [],
        is_new: true,
        visibility: "Public"
      };
      add_item = function(self) {
        var item;
        if ('items' in self) {
          item = Item.$build(Item.init);
          item.owner = Auth.get_user().id;
          item.is_new = true;
          self['items'].push(item);
          return item;
        }
      };
      is_valid = function(self) {
        var item, _i, _len, _ref;
        if (!self.title || !self.area) {
          return false;
        }
        _ref = self.items;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          item = _ref[_i];
          if (item.title.length === 0) {
            return false;
          }
        }
        if (self.visibility === "Invitation" && !self.secret_key) {
          return false;
        }
        return true;
      };
      search = function(self, params) {
        var $then, posts;
        posts = self.$search(params);
        return $then = posts.$then(function(response) {
          var i, item, post, _i, _len, _results;
          _results = [];
          for (_i = 0, _len = posts.length; _i < _len; _i++) {
            post = posts[_i];
            if ("tags" in post) {
              if (typeof post.tags === "string") {
                if (post.tags) {
                  post.tags = post.tags.split(",");
                } else {
                  post.tags = [];
                }
              }
            }
            _results.push((function() {
              var _j, _ref, _results1;
              _results1 = [];
              for (i = _j = 0, _ref = post.items.length; 0 <= _ref ? _j < _ref : _j > _ref; i = 0 <= _ref ? ++_j : --_j) {
                item = post.items[i];
                post.items[i] = Item.transform(item);
                if (item.tags != null) {
                  if (typeof item.tags === "string") {
                    if (item.tags) {
                      _results1.push(item.tags = item.tags.split(","));
                    } else {
                      _results1.push(item.tags = []);
                    }
                  } else {
                    _results1.push(void 0);
                  }
                } else {
                  _results1.push(void 0);
                }
              }
              return _results1;
            })());
          }
          return _results;
        });
      };
      visibility_choices = ["Private", "Public", "Invitation"];
      return Model.create('/posts/').mix({
        $extend: {
          Record: {
            visibility_choices: visibility_choices,
            add_item: function() {
              return add_item(this);
            },
            is_valid: function() {
              return is_valid(this);
            },
            initialize: function() {
              return initialize(this);
            },
            pre_save_handler: function() {
              var item, self, _i, _len, _ref, _results;
              self = this;
              if (self.visibility !== "Invitation") {
                self.secret_key = "";
              }
              if ("tags" in self) {
                if (typeof self.tags === "object") {
                  self.tags = self.tags.join(",");
                }
              }
              if (self.items != null) {
                _ref = self.items;
                _results = [];
                for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                  item = _ref[_i];
                  if (item.tags != null) {
                    if (typeof item.tags === "object") {
                      item.tags = item.tags.join(",");
                    }
                  }
                  if (item.tags_private != null) {
                    if (typeof item.tags_private === "object") {
                      _results.push(item.tags_private = item.tags_private.join(","));
                    } else {
                      _results.push(void 0);
                    }
                  } else {
                    _results.push(void 0);
                  }
                }
                return _results;
              }
            }
          },
          Model: {
            search: function(params) {
              return search(this, params);
            },
            init: init
          }
        }
      });
    }
  ]).factory("Item", [
    "Model", "settings", "Handlers", function(Model, settings, Handlers) {
      var availability_choices, condition_choices, customized_fields_cleaner, init, is_valid, utilization_choices, visibility_choices;
      condition_choices = ["Inapplicable", "New", "Like new", "Good", "Functional", "Broken"];
      visibility_choices = ["Public", "Private", "Ex-owners"];
      availability_choices = ["Available", "In use", "Lent", "Given away", "Disposed"];
      utilization_choices = ["Inapplicable", "Daily", "Frequent", "Sometimes", "Rarely", "Never"];
      init = {
        title: "",
        quantity: 1,
        condition: "Good",
        utilization: "Sometimes",
        visibility: "Private",
        available: "No",
        status: "",
        new_status: "",
        expanded: false,
        is_new: false
      };
      customized_fields_cleaner = function(field_type, field_transformer) {
        var field, fields, index, _i, _len, _results;
        if (field_type in self) {
          if (self[field_type]) {
            fields = self[field_type];
            _results = [];
            for (_i = 0, _len = fields.length; _i < _len; _i++) {
              field = fields[_i];
              if (!(field.value && field.title)) {
                index = fields.indexOf(field);
                _results.push(self.customized_num_fields.splice(index, 1));
              } else {
                if (field_transformer != null) {
                  _results.push(field_transformer(field));
                } else {
                  _results.push(void 0);
                }
              }
            }
            return _results;
          }
        }
      };
      is_valid = function(self) {
        if (!self.title) {
          false;
        }
        return true;
      };
      return Model.create("/items/").mix({
        $extend: {
          Record: {
            condition_choices: condition_choices,
            availability_choices: availability_choices,
            visibility_choices: visibility_choices,
            utilization_choices: utilization_choices,
            initialize: function() {
              return initialize(this);
            },
            is_valid: function() {
              return is_valid(this);
            },
            pre_save_handler: function() {
              var self;
              self = this;
              if ("new_owner" in self) {
                if (self["new_owner"]) {
                  self.owner = self['new_owner'].id;
                }
              }
              if (self.new_status) {
                self.status = self.new_status;
              }
              if ("tags" in self) {
                if (typeof self.tags === "object") {
                  self.tags = self.tags.join(",");
                }
              }
              if ("tags_private" in self) {
                if (typeof self.tags_private === "object") {
                  self.tags_private = self.tags_private.join(",");
                }
              }
              customized_fields_cleaner("customized_fields_cleaner", function(field) {
                return field.value = parseFloat(field.value);
              });
              return customized_fields_cleaner("customized_num_fields");
            },
            images_handler: function() {
              return Handlers.images_handler(this);
            },
            tags_handler: function() {
              return Handlers.tags_handler(this);
            },
            add_customized_char_field: function() {
              if (!this.customized_char_fields) {
                this.customized_char_fields = [];
              }
              return this.customized_char_fields.push({
                title: "",
                value: ""
              });
            },
            add_customized_color_field: function() {
              if (!this.customized_color_fields) {
                this.customized_color_fields = [];
              }
              return this.customized_color_fields.push({
                title: "",
                value: ""
              });
            },
            add_customized_num_field: function() {
              if (!this.customized_num_fields) {
                this.customized_num_fields = [];
              }
              return this.customized_num_fields.push({
                title: "",
                value: "",
                unit: ""
              });
            }
          },
          Model: {
            init: init
          }
        }
      });
    }
  ]).factory("BulkItems", [
    "Model", function(Model) {
      return Model.create("/bulk-items/");
    }
  ]).factory("Feed", [
    "Model", function(Model) {
      return Model.create("/feeds/").mix({
        $extend: {
          record: ""
        }
      });
    }
  ]).factory("Timeline", [
    "Model", function(Model) {
      return Model.create("/timeline/");
    }
  ]).factory("ItemTimeline", [
    "Model", function(Model) {
      return Model.create("/timeline/item/");
    }
  ]).factory("UserTimeline", [
    "Model", function(Model) {
      return Model.create("/timeline/user/");
    }
  ]).factory("Transaction", [
    "Model", function(Model) {
      return Model.create("/transactions/").mix({
        $extend: {
          Record: {
            is_valid: function() {
              return true;
            },
            pre_save_handler: function() {
              this.giver = this.giver.id;
              this.receiver = this.receiver.id;
              return this.item = this.item.id;
            },
            revoke: function() {
              this.status = "Revoked";
              return this.save().$then(function() {
                return location.reload();
              });
            },
            dismiss: function() {
              this.status = "Dismissed";
              return this.save().$then(function() {
                return location.reload();
              });
            },
            receive: function() {
              this.status = "Received";
              return this.save().$then(function() {
                return location.reload();
              });
            }
          }
        }
      });
    }
  ]).factory("Update", [
    "Model", function(Model) {
      return Model.create("/updates/");
    }
  ]).factory("InfiniteScroll", [
    "settings", "Handlers", function(settings, Handlers) {
      var InfiniteScroll;
      return InfiniteScroll = (function() {
        InfiniteScroll.prototype.model_types = [];

        InfiniteScroll.prototype.init_starts = void 0;

        InfiniteScroll.prototype.monitor = 0;

        function InfiniteScroll(Model) {
          this.success_handler = __bind(this.success_handler, this);
          this.load = __bind(this.load, this);
          this.params = __bind(this.params, this);
          this.config = __bind(this.config, this);
          this.Model = Model;
        }

        InfiniteScroll.prototype.config = function(configs) {
          var cf, _results;
          _results = [];
          for (cf in configs) {
            _results.push(this[cf] = configs[cf]);
          }
          return _results;
        };

        InfiniteScroll.prototype.tags_handler = function(container) {
          if (container.tags != null) {
            if (container.tags_handler != null) {
              return container.tags_handler();
            } else {
              return Handlers.tags_handler(container);
            }
          }
        };

        InfiniteScroll.prototype.images_handler = function(container) {
          if (container.images != null) {
            if (container.images_handler != null) {
              return container.images_handler();
            } else {
              return Handlers.images_handler(container);
            }
          }
        };

        InfiniteScroll.prototype.params = function(model) {
          var key, params;
          if (model == null) {
            if (this.model_types.length > 1) {
              params = {
                starts: this.init_starts
              };
            } else {
              params = {
                start: this.init_starts
              };
            }
          } else {
            if (this.model_types.length > 1) {
              params = {
                starts: model.starts
              };
            } else {
              params = {
                start: model.start
              };
            }
          }
          if (this.extra_params != null) {
            for (key in this.extra_params) {
              params[key] = this.extra_params[key] || "";
            }
          }
          return params;
        };

        InfiniteScroll.prototype.load = function(model) {
          var params;
          params = this.params(model);
          if (model == null) {
            return this.Model.search(params);
          } else {
            return model.fetch(params);
          }
        };

        InfiniteScroll.prototype.success_handler = function(response) {
          var item, model_name, record, _i, _j, _len, _len1, _ref;
          if (this.model_types.length === 1) {
            response.start = parseInt(this.init_starts) + response.length;
            if (response.tags_handler != null) {
              response.tags_handler();
            }
            if (response.images_handler != null) {
              response.images_handler();
            }
          } else if (this.model_types.length > 1) {
            response.starts = {};
            for (model_name in this.init_starts) {
              response.starts[model_name] = this.init_starts[model_name];
            }
            for (_i = 0, _len = response.length; _i < _len; _i++) {
              record = response[_i];
              model_name = record.model_name;
              response.starts[model_name] += 1;
              if (record.items != null) {
                if (record.items.length) {
                  _ref = record.items;
                  for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
                    item = _ref[_j];
                    this.tags_handler(item);
                    this.images_handler(item);
                  }
                }
              }
              if (record.item != null) {
                this.tags_handler(record.item);
                this.images_handler(record.item);
              }
            }
          }
          return response;
        };

        return InfiniteScroll;

      })();
    }
  ]).factory("Image", [
    "Model", function(Model) {
      return Model.create("/images/").mix();
    }
  ]).factory("Profile", [
    "Model", function(Model) {
      return Model.create("/profiles/").mix({
        $extend: {
          Record: {
            pre_save_handler: function() {
              var categories, self, tag;
              self = this;
              self.accept_donations_categories = '';
              if (self.tags_accept_donations_categories) {
                categories = [
                  (function() {
                    var _i, _len, _ref, _results;
                    _ref = self.tags_accept_donations_categories;
                    _results = [];
                    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                      tag = _ref[_i];
                      _results.push(tag.text);
                    }
                    return _results;
                  })()
                ];
                return self.accept_donations_categories = categories.join(",");
              }
            },
            tags_handler: function() {
              var self, tag;
              self = this;
              self.tags_accept_donations_categories = [];
              console.log("A");
              if (self.accept_donations_categories) {
                console.log("B");
                return self.tags_accept_donations_categories = [
                  (function() {
                    var _i, _len, _ref, _results;
                    _ref = self.accept_donations_categories.split(",");
                    _results = [];
                    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                      tag = _ref[_i];
                      _results.push({
                        text: tag
                      });
                    }
                    return _results;
                  })()
                ][0];
              }
            },
            is_valid: function() {
              return true;
            }
          }
        }
      });
    }
  ]).factory("Auth", [
    "Profile", "Alert", function(Profile, Alert) {
      var profile;
      profile = {};
      return {
        fetch_profile: function() {
          return Profile.search().$asPromise();
        },
        store_profile: function(response) {
          return profile = response;
        },
        get_profile: function() {
          return profile;
        }
      };
    }
  ]);

}).call(this);
