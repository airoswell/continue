angular.module "continue"

.controller "activitySignUpCtrl", [
  "$scope", "Alert", "Attendant",
  ($scope, Alert, Attendant)->

    $scope.is_comming = "Yes"
    $scope.level = "Inapplicable"
    $scope.layout = {
      filter: ""
      submitting: false
    }

    $scope.new_attendants = []

    $scope.$watch "activity", ()->
      Attendant.statistics($scope.activity).$then (response)->
        $scope.statistics = response[0]

    $scope.submit = ()->
      if $scope.layout.submitting
        Alert.show_msg("We are submitting your registration. Please wait.")
      attendant = Attendant.$build(
        name: $scope.name
        email: $scope.email
        is_comming: $scope.is_comming
        activity: $scope.activity
        level: $scope.level
        department: $scope.department
      )
      $scope.layout.submitting = true
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