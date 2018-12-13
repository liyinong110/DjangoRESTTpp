from rest_framework.permissions import BasePermission

from Viewer.models import ViewerUser


class ViewerUserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            return isinstance(request.user, ViewerUser)

        return True