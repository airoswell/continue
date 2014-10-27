console.log("main.js")

app = angular.module('PassOn', []);

app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('Item', function(){
  return function Item(title, quantity){
    this.title = title;
    this.quantity = quantity,
    this.detail = ""
    this.condition = "Gd"
    this.link = ""
  }
});

app.factory('ItemSet', ['Item', function(Item){
  // initialization
  item_set = [];
  var new_item = new Item("", 1);
  item_set.push(new_item);

  return function ItemSet(){
    this.items = item_set;
    this.add_item = function(){
      var new_item = new Item("", 1);
      this.items.push(new_item);
    }
  }
}]);
