angular.module "continue"

.factory 'Alert', ["$rootScope", "$timeout", ($rootScope, $timeout) ->

  alert = {
    is_show_msg: false
    is_show_error: false
    msg: undefined
    error: undefined
  }

  close_alert = ()->
    """
    First 
    """
    alert.show = false
    $timeout ()->
      alert.msg = undefined
      alert.error = undefined
    , 1000

  show_alert = (delay) ->
    this.close_alert()
    alert.show = true
    $timeout close_alert, delay

  return {
    get_msg: () ->
      alert.msg
    get_error: () ->
      alert.error
    is_show_error: () ->
      alert.is_show_error
    is_show_msg: () ->
      alert.is_show_msg
    show_msg: (content, delay) ->
      delay = if delay? then delay else 2000
      alert.msg = content
      alert.is_show_msg = true
      $timeout ()->
        alert.is_show_msg = undefined
        $timeout () ->
          alert.msg = undefined
        , 200
      , delay
    show_error: (content, delay) ->
      delay = if delay? then delay else 10000
      alert.error = content
      alert.is_show_error = true
      $timeout ()->
        alert.is_show_error = false
        $timeout () ->
          alert.error = undefined
        , 200
      , delay
  }
]
.directive "simpleAlert", ["$rootScope", "Alert", ($rootScope, Alert)->
  restrict: "A"
  templateUrl: "/static/app/scripts/services/alert/alert.html"
  link: (scope, element, attrs) ->
    scope.alert = Alert
]