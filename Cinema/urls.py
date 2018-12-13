from django.conf.urls import url

from Cinema import views

urlpatterns = [
    url(r'^users/', views.CinemaUsersAPIView.as_view()),
    url(r'^movieorders/$', views.CinemaMovieOrdersAPIView.as_view()),
    url(r'^movieorders/(?P<pk>\d+)/', views.CinemaMovieOrderAPIView.as_view()),
    url(r'^orderpay/$', views.OrderPayAPIView.as_view()),
    url(r'^orderpayconfirm/', views.order_pay_confirm),
    url(r'^orderpayed/', views.order_payed),
    url(r'^cinemas/', views.CinemasAPIView.as_view()),
    url(r'^halls/', views.HallsAPIView.as_view()),
    url(r'^paidangs/', views.PaiDangsAPIView.as_view()),
]