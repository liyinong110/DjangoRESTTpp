from django.core.cache import cache
from rest_framework.exceptions import APIException, NotFound, AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from DjangoRESTTpp.settings import VIEWER_USER_TIMEOUT
from Viewer.models import ViewerUser
from Viewer.serializers import ViewerUserSerializer
from utils.user_token_util import generate_viewer_token


class ViewerUSerAPIView(CreateAPIView):

    queryset = ViewerUser.objects.all()
    serializer_class = ViewerUserSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "register":
            return self.create(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        else:
            raise APIException(detail="错误的动作")

    def do_login(self, request, *args, **kwargs):

        v_username = request.data.get("v_username")
        v_password = request.data.get("v_password")

        users = ViewerUser.objects.filter(v_username=v_username)

        if not users.exists():
            raise NotFound(detail="对象未找到")

        user = users.first()

        if not user.check_password(v_password):
            raise AuthenticationFailed(detail="密码错误")

        token = generate_viewer_token()

        cache.set(token, user.id, timeout=VIEWER_USER_TIMEOUT)

        data = {
            "msg": "ok",
            "status": HTTP_200_OK,
            "token": token
        }

        return Response(data)


