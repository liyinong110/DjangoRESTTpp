import datetime

from rest_framework.generics import ListCreateAPIView

from Cinema.models import PaiDang
from Viewer.authentications import ViewerUserAuthentication
from Viewer.models import ViewerOrder
from Viewer.permissions import ViewerUserPermission
from Viewer.serializers import ViewerOrderSerializer


class ViewerOrdersAPIView(ListCreateAPIView):

    queryset = ViewerOrder.objects.all()
    serializer_class = ViewerOrderSerializer
    authentication_classes = (ViewerUserAuthentication,)
    permission_classes = (ViewerUserPermission,)

    def post(self, request, *args, **kwargs):

        v_user_id = request.user.id
        v_paidang_id = request.data.get("v_paidang_id")
        v_seats = request.data.get("v_seats")

        seat_count = len(v_seats.split("#"))

        paidang = PaiDang.objects.get(pk=v_paidang_id)

        v_single_price = paidang.p_price

        v_price = v_single_price * seat_count

        request.v_user_id = v_user_id
        request.v_price = v_price
        request.v_paidang_id = v_paidang_id
        request.v_seats = v_seats

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        expire_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
        serializer.save(v_expire= expire_time,v_seats=self.request.v_seats, v_price=self.request.v_price, v_paidang_id=self.request.v_paidang_id,v_user_id=self.request.v_user_id)

