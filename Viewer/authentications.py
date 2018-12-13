from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from Viewer.models import ViewerUser


class ViewerUserAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            token = request.query_params.get("token")
            viewer_id = cache.get(token)
            viewer_user = ViewerUser.objects.get(pk=viewer_id)
            return viewer_user, token
        except Exception as e:
            print("认证失败", e)
            return None