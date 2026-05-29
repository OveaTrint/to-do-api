from rest_framework.exceptions import PermissionDenied


def is_owner_of_todo(request, obj):
    """Checks whether the requesting user is the authorized user"""
    if request.user != obj.owner:
        raise PermissionDenied()
    return True
