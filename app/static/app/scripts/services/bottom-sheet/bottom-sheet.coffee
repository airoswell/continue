angular.module "continue"

.factory "BottomSheet", ["Item", (Item) ->
  return{
    item: undefined
    items: undefined
    is_show: false
    show: (item)->
      this.is_show = true
      this.item = item
      if "id" of item
        return this
      else
        this.items = Item.$search({page: 1, num_of_records: 10})
        return this

    close: ()->
      this.is_show = false
      return this

    select: (item, existing_item)->
      for prop of existing_item
        item[prop] = existing_item[prop]
      item.is_new = false
  }
]

.directive "bottomSheet", ["BottomSheet", (BottomSheet)->
  return {
    restrict: "E"
    templateUrl: "/static/app/scripts/services/bottom-sheet/bottom-sheet.html"
    link: (scope, element, attrs) ->
      scope.layout = {
        selected: false
      }
      scope.BottomSheet = BottomSheet
      scope.$watch "BottomSheet.item", ()->
        scope.item = BottomSheet.item
        scope.items = BottomSheet.items
      scope.select = (item, existing_item)->
        BottomSheet.select(item, existing_item)
        scope.layout.selected = true
  }
]

