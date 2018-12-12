import uuid

from django.core.cache import cache
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from Admin.authentication import AdminUserAuthentication
from Cinema.models import CinemaUser
from Cinema.permissions import AdminUserPermission
from Cinema.serializers import CinemaUserSerializer
from DjangoRESTTpp.settings import CINEMA_USER_TIMEOUT
from utils.user_token_util import generate_cinema_token


class CinemaUsersAPIView(ListCreateAPIView):

    queryset = CinemaUser.objects.all()
    serializer_class = CinemaUserSerializer
    authentication_classes = (AdminUserAuthentication, )
    permission_classes = (AdminUserPermission, )

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "register":
            return self.create(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        else:
            raise APIException(detail="请提供争取动作")

    def do_login(self, request, *args, **kwargs):
        c_username = request.data.get("c_username")
        c_password = request.data.get("c_password")

        users = CinemaUser.objects.filter(c_username=c_username)

        if not users.exists():
            raise APIException(detail="用户不存在")

        user = users.first()

        if not user.check_user_password(c_password):
            raise APIException(detail="密码错误")

        if user.is_delete:
            raise APIException(detail="用户已删除")

        token = generate_cinema_token()

        cache.set(token, user.id, timeout=CINEMA_USER_TIMEOUT)

        data = {
            "msg": "ok",
            "status": HTTP_200_OK,
            "token": token
        }
        return Response(data)