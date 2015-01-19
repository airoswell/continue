app = angular.module("continue", [
  "ngResource"
  "ngAria"
  "ngAnimate"
  "ngMaterial"
  "restmod"
  "continue.auth"
  "continue.models"
  "continue.social_accounts"
  "ngTagsInput"
  "infinite-scroll"
  "hc.marked"
])

app.config [
  "$httpProvider"
  ($httpProvider) ->
    $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest"
    # $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded"
    $httpProvider.defaults.xsrfCookieName = "csrftoken"
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"
]
app.config [
  'markedProvider'
  (markedProvider)->
    markedProvider.setOptions({gfm: true});
]
