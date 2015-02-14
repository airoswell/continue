angular.module "continue"

.controller "activitySignUpCtrl", [
  "$scope", "Alert", "Attendant",
  ($scope, Alert, Attendant)->

    $scope.is_comming = "Yes"

    $scope.new_attendants = []

    $scope.submit = ()->
      console.log "submit"
      attendant = Attendant.$build(
        name: $scope.name
        email: $scope.email
        is_comming: $scope.is_comming
        activity: $scope.activity
      )
      attendant.save().$then (response)->
        $scope.new_attendants.push(response)

]