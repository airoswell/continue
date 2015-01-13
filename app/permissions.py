from rest_framework import permissions


class IsOwnerOrNoPermission(permissions.BasePermission):
    """
        Only the owner can perform any request on it.
        Typically apply to an <item>.
        Return 401 UNAUTHORIZED when a user (not the owner) make a
        request.
    """
    def has_object_permission(self, request, view, instance=None):
        try:
            return instance.owner == request.user
        except AttributeError:
            return instance.item.owner == request.user
        else:
            return


class IsSelfOrNoPermission(permissions.BasePermission):
    """
        Only the user himself can retrieve the his own user profile.
    """
    def has_object_permission(self, request, view, instance=None):
        try:
            return instance.user == request.user
        except AttributeError:
            return False


class IsGiverOrReceiverOrNoPermission(permissions.BasePermission):
    """
    Only the two parties of a transaction can view the detail
    """
    def has_object_permission(self, request, view, instance=None):
        try:
            user = request.user
            permission = (user == instance.giver or user == instance.receiver)
            return permission
        except:
            return False


class IsOwnerOrPublicOrNoPermission(permissions.BasePermission):
    """
        Only the owner can perform any request on it.
        Typically apply to an <item>.
        Return 401 UNAUTHORIZED when a user (not the owner) make a
        request.
    """
    def has_object_permission(self, request, view, instance=None):
        try:
            if request.method in permissions.SAFE_METHODS:
                permission = ((instance.owner == request.user) or
                              instance.visibility == 'Public')
            else:
                permission = instance.owner == request.user
            return permission
        except AttributeError:
            if request.method in permissions.SAFE_METHODS:
                permission = ((instance.item.owner == request.user) or
                              instance.item.visibility == 'Public')
            else:
                permission = instance.item.owner == request.user
            return permission
        else:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Only the owner can perform PUT/POST/DELETE request on it.
        Typically apply to an item.
    """
    def has_object_permission(self, request, view, instance=None):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return instance.owner == request.user
