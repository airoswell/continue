angular.module "worldsheet"

.controller "activitySignUpCtrl", [
  "$scope", "$q", "Alert", "Attendant",
  ($scope, $q, Alert, Attendant)->

    $scope.is_comming = "Yes"
    $scope.level = "Inapplicable"
    $scope.layout = {
      filter: ""
      submitting: false
      submited: false
    }

    $scope.fields = Attendant.fields()

    $scope.load_fields = ()->
      deferred = $q.defer()
      console.log deferred
      deferred.resolve($scope.fields)
      return deferred.promise


    $scope.new_attendants = []

    unwatch = $scope.$watch "date", ()->
      console.log "$scope.date", $scope.date
      $scope.date = Date.parse($scope.date)
      console.log "$scope.date", $scope.date
      unwatch()

    $scope.$watch "activity", ()->
      Attendant.statistics($scope.activity, $scope.date).$then (response)->
        $scope.statistics = response[0]

    $scope.submit = ()->
      if $scope.layout.submitting
        Alert.show_msg("We are submitting your registration. Please wait.")
      fields = [tag.text for tag in $scope.interested_in_fields_tags].join(",")
      console.log "fields", fields
      attendant = Attendant.$build(
        name: $scope.name
        email: $scope.email
        is_comming: $scope.is_comming
        level: $scope.level
        department: $scope.department
        activity: $scope.activity
        date: $scope.date
        fields: fields
      )
      $scope.layout.submitting = true
      attendant.save().$then (response)->
        $scope.new_attendants.push(response)
        top = $("#response").offset().top
        $("html, body").animate "scrollTop": top
        $scope.fields = Attendant.fields()
        Attendant.statistics($scope.activity, $scope.date).$then (response)->
          $scope.statistics = response[0]
        $scope.layout.submited = true

    $scope.filter = (decision)->
      if $scope.layout.filter == decision
        $scope.layout.filter = ""
      else
        $scope.layout.filter = decision

]