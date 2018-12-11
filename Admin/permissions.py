from rest_framework.permissions import BasePermission

from Admin.models import AdminUser


class CreatePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        # if isinstance(user, AdminUser) and user.is_super:
        #     return True
        # return False
        return isinstance(user, AdminUser) and user.is_super