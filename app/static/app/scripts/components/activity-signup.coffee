angular.module "continue"

.controller "activitySignUpCtrl", [
  "$scope", "Alert", "Attendant",
  ($scope, Alert, Attendant)->

    $scope.is_comming = "Yes"
    $scope.level = "Inapplicable"
    $scope.layout = {
      filter: ""
    }

    $scope.new_attendants = []

    $scope.$watch "activity", ()->
      Attendant.statistics($scope.activity).$then (response)->
        $scope.statistics = response[0]

    $scope.submit = ()->
      console.log "submit"
      attendant = Attendant.$build(
        name: $scope.name
        email: $scope.email
        is_comming: $scope.is_comming
        activity: $scope.activity
        level: $scope.level
        department: $scope.department
      )
      attendant.save().$then (response)->
        $scope.new_attendants.push(response)
        Attendant.statistics().$then (response)->
          $scope.statistics = response[0]

    $scope.filter = (decision)->
      if $scope.layout.filter == decision
        $scope.layout.filter = ""
      else
        $scope.layout.filter = decision

]