from django.conf.urls import url

from Cinema import views

urlpatterns = [
    url(r'^users/', views.CinemaUsersAPIView.as_view()),
]