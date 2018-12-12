from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from Admin.models import AdminUser
from utils.user_token_util import ADMIN


class AdminUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get("token")

            if not token.startswith(ADMIN):
                raise Exception("错误的操作")

            user_id = cache.get(token)
            user = AdminUser.objects.get(pk=user_id)
            return user,token

        except Exception as e:
            print("认证失败", e)
            return None