angular.module "continue"

.controller "messageViewCtrl", ["$scope", ($scope)->
  $scope.reply = ()->
    console.log $("[name='replyForm']")
    $("[name='replyForm']").submit()

  $scope.delete = ()->
    
]