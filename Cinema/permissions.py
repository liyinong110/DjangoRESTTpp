from rest_framework.exceptions import APIException
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

        if type(view).__name__ == "HallsAPIView":

            h_cinema_id = request.data.get("h_cinema_id") or request.query_params.get("h_cinema_id")

            cinemas = request.user.cinema_set.filter(pk=h_cinema_id)

            if not cinemas.exists():
                raise APIException(detail="请选择正确的影院")
            request.h_cinema_id = h_cinema_id

            user = request.user
            return isinstance(user, CinemaUser)
        else:

            if request.method == "POST":
                user = request.user
                return isinstance(user, CinemaUser)

        return True