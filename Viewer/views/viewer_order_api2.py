import datetime

from django.core.cache import caches
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from Cinema.models import PaiDang
from Viewer.authentications import ViewerUserAuthentication
from Viewer.controller import get_valid_seats
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

        cache = caches["default"]
        # print(cache)
        # print(type(cache))

        # key = "paidang_id" +"lock"+ "seat_num"
        # cache.get()
        v_seat_list = v_seats.split("#")

        for v_seat in v_seat_list:
            result = cache.get(v_paidang_id + "lock" + v_seat)
            if result:
                raise APIException(detail="lock fail")

        for v_seat in v_seat_list:
            cache.set(v_paidang_id + "lock" + v_seat, "lock", timeout=15*60)

        data = {
            "msg": "debuging"
        }

        return Response(data)



        # 判定提供的座位是不是可用的

        valid_seats = get_valid_seats(v_paidang_id)

        v_seats_set = set(v_seats.split("#"))

        request.v_seats_set = v_seats_set

        if set(valid_seats) & v_seats_set != v_seats_set:
            raise APIException(detail="锁座失败")

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

        # 判定什么？  检测除自己的订单外，还有没有其它订单包含我们的座位
        print(serializer.instance.id)
        valid_seats = get_valid_seats(self.request.v_paidang_id, order_id=serializer.instance.id)
        #
        v_seats_set = self.request.v_seats_set
        if set(valid_seats) & v_seats_set != v_seats_set:
              # 以自己的时间（之前），座位去查找， 找到就删除自己
            viewerorders = ViewerOrder.objects.filter(self.request.v_paidang_id).filter(v_expire__lt=serializer.instance.v_expire)

            orders_seats = []

            for viewer_order in viewerorders:
               orders_seats += viewer_order.v_seats.split("#")

            if set(orders_seats) & v_seats_set:
                serializer.instance.delete()
                raise APIException(detail="锁单失败，有人比你手快")
