app = angular.module("continue", [
  "ngResource"
  "ngAria"
  "ngAnimate"
  "ngMaterial"
  "restmod"
  "ui.bootstrap"
  "continue.auth"
  "continue.models"
  "continue.social_accounts"
  # some nice angular widgets
  "ngTagsInput"
  "infinite-scroll"
  "hc.marked"
  "omr.angularFileDnD"
])

app.config [
  "$httpProvider"
  ($httpProvider) ->
    $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest"
    $httpProvider.defaults.xsrfCookieName = "csrftoken"
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"
]
app.config [
  'markedProvider'
  (markedProvider)->
    markedProvider.setOptions({gfm: true});
]

app.factory "settings", ()->
  HOST_URL = "http://104.237.144.150"
  # HOST_URL = "http://localhost:8000"
  STATIC_URL = "#{HOST_URL}/static"
  UPLOADED_URL = "#{STATIC_URL}/uploaded/"
  return {
    STATIC_URL: STATIC_URL
    UPLOADED_URL: UPLOADED_URL
  }
