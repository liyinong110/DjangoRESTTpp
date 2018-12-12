from rest_framework.permissions import BasePermission

from Admin.models import AdminUser
from Cinema.models import CinemaUser


class AdminUserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == "GET":

            user = request.user

            return isinstance(user, AdminUser)
        return True


class CinemaMovieOrderPermission(BasePermission):

    CINEMA_USER_METHODS = ["POST", "DELETE"]

    def has_permission(self, request, view):
        if request.method == "GET":
            user = request.user

            return isinstance(user, AdminUser) or isinstance(user, CinemaUser)
        elif request.method in self.CINEMA_USER_METHODS:

            user = request.user

            return isinstance(user, CinemaUser)
        return False


class CinemaPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            user = request.user
            return isinstance(user, CinemaUser)
        return True