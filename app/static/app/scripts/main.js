console.log("main.js")

app = angular.module('Continue', []);

app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('Item', function(){
  return function Item(item_data){
    if (Object.getOwnPropertyNames(item_data) == 0){
      this.item_id = "undefined";
      this.owner_id = "undefined";
      this.title = "";
      this.quantity = 1;
      this.detail = "";
      this.condition = "Gd";
      this.link = "";
      this.status = 'av';
    }
    else{
      this.item_id = item_data.item_id;
      this.owner_id = item_data.owner_id;
      this.title = item_data.title;
      this.quantity = item_data.quantity;
      this.detail = item_data.detail;
      this.condition = item_data.condition;
      this.link = item_data.link;
      this.status = item_data.status;
    }
  }
});

app.factory('ItemSet', ['Item', function(Item){
  // initialization
  item_set = [];
  var new_item = new Item({});
  item_set.push(new_item);

  return function ItemSet(){
    this.items = item_set;
    this.add_item = function(){
      var new_item = new Item({});
      this.items.push(new_item);
    }
  }
}]);

app.factory('Http', ['$http', function($http){
  return{
    request: function(method, url, data, success_handler){
      $http({
        method: method,
        url: url,
        data: data,
      }).success(function(data, status, headers, config){
        success_handler(data, status, headers, config);
      })
    }
  }
}])
