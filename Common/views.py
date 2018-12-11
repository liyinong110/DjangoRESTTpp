from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from Admin.authentication import AdminUserAuthentication
from Admin.permissions import SuperAdminUserPermission
from Common.models import Movie
from Common.serializers import MovieSerializer


class MoivesAPIView(ListCreateAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (AdminUserAuthentication,)
    permission_classes = (SuperAdminUserPermission,)