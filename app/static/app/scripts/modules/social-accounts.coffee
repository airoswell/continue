angular.module "continue.social_accounts", [
  "continue.auth"
  "continue.social_accounts.facebook"
]

angular.module "continue.social_accounts.facebook", [
  "ngResource"
]

angular.module "continue.social_accounts.facebook"

.factory "FB", ["$resource", "Auth", ($resource, Auth)->

  window.fbAsyncInit = ()->
    FB.init
      appId: "838251579531523"
      xfbml: true
      version: "v2.1"
    return

  ((d, s, id) ->
    js = undefined
    fjs = d.getElementsByTagName(s)[0]
    return  if d.getElementById(id)
    js = d.createElement(s)
    js.id = id
    js.src = "//connect.facebook.net/en_US/sdk.js"
    fjs.parentNode.insertBefore js, fjs
    return
  ) document, "script", "facebook-jssdk"
  init = (provider)->
    if provider is "Facebook"
      window.fbAsyncInit = ()->
        FB.init
          appId: "838251579531523"
          xfbml: true
          version: "v2.1"
        return

      ((d, s, id) ->
        js = undefined
        fjs = d.getElementsByTagName(s)[0]
        return  if d.getElementById(id)
        js = d.createElement(s)
        js.id = id
        js.src = "//connect.facebook.net/en_US/sdk.js"
        fjs.parentNode.insertBefore js, fjs
        return
      ) document, "script", "facebook-jssdk"

  resource = $resource(
    "https://graph.facebook.com/v2.2/:node/:id/:edge"
  )

  return{
    get_user: ()->
      resource.get({
        node:"me"
        access_token: Auth.get_user().social_account_access_token
      }, (response)->
        console.log "facebook response", response
      ).$promise
    init: (provider) ->
      init(provider)

    resource: resource
  }
]
