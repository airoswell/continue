angular.module "continue"

.factory "PrivateMessage", ["restmod", "Auth", "BS", "Alert", (restmod, Auth, BS, Alert)->
  PM = restmod.model("/user/messages/").mix(
    $hooks:
      'before-request': (_req)->
        _req.url += "/"
  )
  return {
    pm: PM.$build()
    monitor: 0      # used for PrivateMessageCtrl to monitor change in
                    # this factory
    deferred: {}
    compose: (owner_id, post_id, items)->
      self = this
      self.monitor += 1
      self.pm.recipient = owner_id
      self.pm.post_id = post_id
      self.pm.items = items     # only store id of items
      user = Auth.get_user()
      if not user.is_anonymous
        self.pm.sender = user.id
      else
        self.pm.sender = "ai.roswell@gmail.com"
      self.deferred = BS.bringUp("private-message")

    send: (subject, body)->
      self = this
      Alert.show_msg("Sending your message ...")
      this.pm.subject = subject
      this.pm.body = body
      this.pm.$save().$then (response)->
        Alert.show_msg("Messages is sent successfully!")
        self.deferred.resolve()
      self.deferred.promise
      location.reload()
  }
]

.controller "privateMessageCtrl",[
  "$scope", "Item", "PrivateMessage"
  ($scope, Item, PrivateMessage)->
    # =================== Initialization ======================
    # Initialize the controller, only run once after the first time
    # the [contact-button] is clicked
    $scope.PrivateMessage = PrivateMessage
    $scope.items = []   # used to display selected items in bottom-sheet
    item_ids = []  # Keep track of already downloaded items
    # =================== Initialization END ======================
    $scope.$watch "PrivateMessage.monitor", ()->
      # [contact-button] in different posts should give different
      # private-message bottom-sheet
      if not $scope.post_id?
        $scope.post_id = PrivateMessage.pm.post_id
      else if $scope.post_id != PrivateMessage.pm.post_id
        $scope.items = []
        item_ids = []
      for item_id in $scope.PrivateMessage.pm.items
        if not (item_id in item_ids)
          item_ids.push(item_id)
          Item.$find(item_id).$then (response)->
            $scope.items.push(response)

    $scope.send = ()->
      PrivateMessage.send($scope.subject, $scope.body).then ()->
        $scope.body = undefined
        $scope.subject = undefined
]