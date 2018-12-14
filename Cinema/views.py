import uuid

from alipay import AliPay
from django.core.cache import cache
from django.db.models import Q
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from Admin.authentication import AdminUserAuthentication
from Cinema.authentication import CinemaUserAuthentication
from Cinema.models import CinemaUser, CinemaMovieOrder, Cinema, Hall, PaiDang, ORDERED_PAYED
from Cinema.permissions import AdminUserPermission, CinemaMovieOrderPermission, CinemaPermission
from Cinema.serializers import CinemaUserSerializer, CinemaMovieOrderSerializer, CinemaSerializer, HallSerializer, PaiDangSerializer
from Common.models import Movie
from DjangoRESTTpp.settings import CINEMA_USER_TIMEOUT, APP_ID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
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


class CinemaMovieOrdersAPIView(ListCreateAPIView):

    queryset = CinemaMovieOrder.objects.all()
    serializer_class = CinemaMovieOrderSerializer
    authentication_classes = (CinemaUserAuthentication, AdminUserAuthentication)
    permission_classes = (CinemaMovieOrderPermission, )

    def get_queryset(self):
        queryset = super(CinemaMovieOrdersAPIView, self).get_queryset()
        user = self.request.user
        if isinstance(user, CinemaUser):
            queryset = queryset.filter(c_user_id=user.id)
        return queryset

    def post(self, request, *args, **kwargs):
        # user = self.request.user
        # user_id = user.id

        movie_id = request.data.get("c_movie_id")
        movie = Movie.objects.get(pk=movie_id)
        c_price = movie.m_price

        self.request.c_price = c_price
        self.request.c_movie_id = movie_id

        orders = CinemaMovieOrder.objects.filter(c_movie_id=movie_id).filter(c_user_id=request.user.id)

        if orders.exists():
            raise APIException(detail="已购买")

        # print(user_id)
        #
        # request_data = {"c_price": c_price, "c_user_id": user_id, "c_movie_id": movie_id}
        #
        # print(request_data)
        #
        # serializer = self.get_serializer(data=request_data)
        # print(serializer)
        # serializer.is_valid(raise_exception=True)
        # print(serializer)

        # 外键级联字段是只读字段，  是不可修改， 想修改值， 自己传输验证后的字段
        # serializer.save(c_price=c_price_, c_user_id=user_id, c_movie_id=movie_id)

        # headers = self.get_success_headers(serializer.data)
        #
        # return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(c_price=self.request.c_price, c_user_id=self.request.user.id, c_movie_id=self.request.c_movie_id)


class CinemaMovieOrderAPIView(RetrieveDestroyAPIView):

    queryset = CinemaMovieOrder.objects.filter(is_delete=False)
    serializer_class = CinemaMovieOrderSerializer
    authentication_classes = (CinemaUserAuthentication,)
    permission_classes = (CinemaMovieOrderPermission, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data={"is_delete":True}, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)


class OrderPayAPIView(GenericAPIView):

    authentication_classes = (CinemaUserAuthentication, )
    permission_classes = (CinemaMovieOrderPermission, )

    def post(self, request, *args, **kwargs):

        order_id = request.data.get("order_id")
        pay_channel = request.data.get("pay_channel")
        order = CinemaMovieOrder.objects.get(pk=order_id)

        o_price = order.c_price

        order_id = "cinema_movie" + order_id

        if pay_channel == "alipay":

            subject = "电脑"

            alipay = AliPay(
                appid=APP_ID,
                app_notify_url=None,
                app_private_key_string=APP_PRIVATE_KEY,
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                alipay_public_key_string=ALIPAY_PUBLIC_KEY,
                sign_type="RSA",
                debug = True  # 默认False
            )

            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order_id,
                total_amount=o_price,
                subject=subject,
                return_url="http://localhost:8000/cinema/orderpayed/",
                notify_url="http://localhost:8000/cinema/orderpayconfirm/"  # 可选, 不填则使用默认notify url
            )

            pay_info = "https://openapi.alipaydev.com/gateway.do?" + order_string

        elif pay_channel == "wechat":
            pay_info = "xxx"
        else:
            pay_info = "yyy"

        data = {
            "msg": "ok",
            "status": 200,
            "pay_url": pay_info
        }

        return Response(data)


@api_view(["GET", "POST"])
def order_pay_confirm(request):

    print(request.data)

    data = {
        "msg": "ok"
    }
    return Response(data)


@api_view(["GET", "POST"])
def order_payed(request):

    data = {
        "msg": "pay success"
    }

    return Response(data)


class CinemasAPIView(ListCreateAPIView):

    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    authentication_classes = (CinemaUserAuthentication, )
    permission_classes = (CinemaPermission, )

    def perform_create(self, serializer):
        serializer.save(c_user_id = self.request.user.id)

    def get_queryset(self):
        queryset = super(CinemasAPIView, self).get_queryset()

        if isinstance(self.request.user, CinemaUser):
            queryset = queryset.filter(c_user = self.request.user)
        return queryset


class HallsAPIView(ListCreateAPIView):

    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    authentication_classes = (CinemaUserAuthentication, )
    permission_classes = (CinemaPermission, )

    def get_queryset(self):
        queryset = super(HallsAPIView, self).get_queryset()
        queryset = queryset.filter(h_cinema_id=self.request.h_cinema_id)
        return queryset

    def perform_create(self, serializer):
        h_cinema_id = self.request.h_cinema_id
        serializer.save(h_cinema_id=h_cinema_id)


class PaiDangsAPIView(ListCreateAPIView):

    queryset = PaiDang.objects.all()
    serializer_class = PaiDangSerializer
    authentication_classes = (CinemaUserAuthentication, )
    permission_classes = (CinemaPermission, )

    # 时间  电影院   电影
    def get(self, request, *args, **kwargs):
        cinema_id = request.query_params.get("cinema_id")
        movie_id = request.query_params.get("movie_id")
        p_time = request.query_params.get("p_time")

        # 验证参数合法性
        request.cinema_id = cinema_id
        request.movie_id = movie_id
        request.p_time = p_time
        return self.list(request, *args, **kwargs)

    def get_queryset(self):

        queryset = super(PaiDangsAPIView,self).get_queryset()

        p_time = self.request.p_time

        year_month_day = p_time

        year, month, day= year_month_day.split("-")

        queryset = queryset.filter(p_cinema_id=self.request.cinema_id).filter(p_movie_id=self.request.movie_id)\
            .filter(p_time__year=year).filter(p_time__month=month).filter(p_time__day=day)

        return queryset

    def post(self, request, *args, **kwargs):
        p_hall_id = request.data.get("p_hall_id")
        p_cinema_id = request.data.get("p_cinema_id")

        cinemas = request.user.cinema_set.filter(pk=p_cinema_id)

        if not cinemas.exists():
            raise APIException(detail="请选择正确的影院")

        cinema = cinemas.first()

        halls = cinema.hall_set.filter(pk=p_hall_id)

        if not halls.exists():
            raise APIException(detail="请选择正确的大厅")

        # 电影是否购买
        # 去订单表中查询   查询当前用户，所购电影
        p_movie_id = request.data.get("p_movie_id")

        orders = CinemaMovieOrder.objects.filter(c_movie_id=p_movie_id).filter(c_user_id=request.user.id).filter(c_status=ORDERED_PAYED)

        if not orders.exists():
            raise APIException(detail="电影未购买")

        movie = Movie.objects.get(pk=p_movie_id)

        # p_time 开始
        p_time = request.data.get("p_time")

        # p_time_end  + 电影时长 + 打扫时长

        times = p_time.split(" ")

        year, month, day = times[0].split("-")
        hour, minute, second = times[1].split(":")

        clean_time = 15

        # p_time_end = p_time + movie.m_duration + 15
        p_time_end = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second)) + datetime.timedelta(minutes=movie.m_duration + clean_time)

        # 写注释
        paidangs = PaiDang.objects.filter(Q(Q(p_time__lte=p_time) & Q(p_time_end__gte=p_time_end)) | Q(Q(p_time_end__gte=p_time) & Q(p_time_end__lte=p_time_end)) | Q(Q(p_time__gte=p_time) & Q(p_time__lte=p_time_end)))

        if paidangs.exists():
            raise APIException(detail="时间冲突")
        # if paidangs.exists():
        #     raise APIException(detail="时间被包含")

        # paidangs = PaiDang.objects.filter(Q(p_time_end__gte=p_time) & Q(p_time_end__lte=p_time_end))
        #
        # if paidangs.exists():
        #     raise APIException(detail="包含结束")
        #
        # paidangs = PaiDang.objects.filter(Q(p_time__gte=p_time) & Q(p_time__lte=p_time_end))
        #
        # if paidangs.exists():
        #     raise APIException(detail="包含开始")

        request.p_movie_id = p_movie_id
        request.p_hall_id = p_hall_id
        request.p_cinema_id = p_cinema_id
        request.p_time_end = "{}-{}-{} {}:{}:{}".format(p_time_end.year,p_time_end.month, p_time_end.day, p_time_end.hour, p_time_end.minute, p_time_end.second)

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(p_time_end=self.request.p_time_end,p_hall_id=self.request.p_hall_id, p_cinema_id=self.request.p_cinema_id, p_movie_id=self.request.p_movie_id)