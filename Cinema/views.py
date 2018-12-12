import uuid

from django.core.cache import cache
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from Admin.authentication import AdminUserAuthentication
from Cinema.authentication import CinemaUserAuthentication
from Cinema.models import CinemaUser, CinemaMovieOrder
from Cinema.permissions import AdminUserPermission, CinemaMovieOrderPermission
from Cinema.serializers import CinemaUserSerializer, CinemaMovieOrderSerializer
from Common.models import Movie
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

    queryset = CinemaMovieOrder.objects.all()
    serializer_class = CinemaMovieOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data={"is_delete":True}, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)


