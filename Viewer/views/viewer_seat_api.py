from rest_framework.response import Response
from rest_framework.views import APIView

from Viewer.authentications import ViewerUserAuthentication
from Viewer.controller import get_valid_seats
from Viewer.permissions import ViewerUserPermission


class SeatsAPIView(APIView):

    authentication_classes = (ViewerUserAuthentication,)
    permission_classes = (ViewerUserPermission, )

    def get(self, request, *args, **kwargs):

        paidang_id = request.query_params.get("paidang_id")

        valid_seats = get_valid_seats(paidang_id)

        data = {
            "msg": "ok",
            "seats": "#".join(valid_seats)
        }

        return Response(data)