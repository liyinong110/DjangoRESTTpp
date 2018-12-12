from rest_framework.permissions import BasePermission

from Admin.models import AdminUser


class AdminUserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == "GET":

            user = request.user

            return isinstance(user, AdminUser)
        return True