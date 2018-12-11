from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from Admin.models import AdminUser
from Admin.serializers import AdminUserSerializer


class AdminUsersAPIView(CreateAPIView):

    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.filter(is_delete=False)