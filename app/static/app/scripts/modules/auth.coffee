angular.module "continue.auth", ["restmod"]

.factory "Auth", ["restmod", (restmod)->
  Profile = restmod.model("/profiles/")
  profile = {}
  return{
    fetch_profile: () ->
      Profile.$search().$asPromise()
    store_profile: (response)->
      profile = response
    get_profile: ()->
      profile
  }
]

