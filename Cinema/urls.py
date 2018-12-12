from django.conf.urls import url

from Cinema import views

urlpatterns = [
    url(r'^users/', views.CinemaUsersAPIView.as_view()),
    url(r'^movieorders/$', views.CinemaMovieOrdersAPIView.as_view()),
    url(r'^movieorders/(?P<pk>\d+)/', views.CinemaMovieOrderAPIView.as_view()),
]