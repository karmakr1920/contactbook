from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Grants access only if the contact's user matches the requesting user.
    """
    message = 'You do not have permission to access this contact.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
