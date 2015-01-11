angular.module "continue.auth", ["restmod"]

.factory "Auth", ["restmod", (restmod)->
  User = restmod.model("/user/")
  user = {}
  return{
    get_user_profile: () ->
      User.$search().$asPromise()
    store_user: (response)->
      user = response
    get_user: ()->
      user
  }
]

