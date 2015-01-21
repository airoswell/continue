angular.module "continue"

.controller "indexCtrl", ["$scope", ($scope)->
  
  $scope.tags_to_string = (input_tags)->
    if input_tags
      areas = [tag.text for tag in input_tags]
      areas = areas.join(",")
      return areas
    return ""
  
  $("input[name='q']").on 

  $("input[name='q'], input[name='secret_key']").keyup (e)->
    if e.which == 13
      $scope.search()

  $scope.search = ()->
    areas = $scope.tags_to_string($scope.areas_tags)
    tags = $scope.tags_to_string($scope.tags_tags)
    $("input[name=areas]").val(areas)
    $("input[name=tags]").val(tags)
    document.getElementById('index-search-form').submit()
    # clear the input to prevent going back and see the input
    $("input").val("")
]