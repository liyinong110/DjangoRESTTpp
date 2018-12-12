import uuid

from django.core.cache import cache
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response

from Admin.authentication import AdminUserAuthentication
from Admin.models import AdminUser, Permission
from Admin.permissions import SuperAdminUserPermission
from Admin.serializers import AdminUserSerializer, PermissionSerializer
from DjangoRESTTpp.settings import ADMIN_USER_TIMEOUT, ADMIN_USERS
from utils.user_token_util import generate_admin_token


class AdminUsersAPIView(CreateAPIView):

    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.filter(is_delete=False)

    def post(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == "register":
            return self.create(request, *args, **kwargs)
        elif action == "login":
            a_username = request.data.get("a_username")
            a_password = request.data.get("a_password")

            users = AdminUser.objects.filter(a_username=a_username)

            if not users.exists():
                raise APIException(detail="用户不存在")

            user = users.first()

            if not user.check_admin_password(a_password):
                raise APIException(detail="密码错误")

            if user.is_delete:
                raise APIException(detail="用户已离职")

            token = generate_admin_token()

            cache.set(token, user.id, timeout=ADMIN_USER_TIMEOUT)

            data = {
                "msg": "ok",
                "status": 200,
                "token": token
            }

            return Response(data)

        else:
            raise APIException(detail="请提供正确的动作")

    def perform_create(self, serializer):
        a_username = self.request.data.get("a_username")

        serializer.save(is_super = a_username in ADMIN_USERS)

        # if a_username in ADMIN_USERS:
        #     serializer.save(is_super=True)
        # else:
        #     serializer.save()


class PermissionsAPIView(ListCreateAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = (AdminUserAuthentication, )
    permission_classes = (SuperAdminUserPermission,)

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        permission_id = request.data.get("permission_id")

        try:
            permission = Permission.objects.get(pk=permission_id)
        except Exception as e:
            print(e)
            raise APIException(detail="权限不存在")

        try:
            user = AdminUser.objects.get(pk=user_id)
        except Exception as e:
            print(e)
            raise APIException(detail="用户不存在")

        user.permission_set.add(permission)

        data = {
            "msg": "add success",
            "status": 201
        }

        return Response(data)