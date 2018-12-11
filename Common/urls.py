from django.conf.urls import url

from Common import views

urlpatterns = [
    url(r'^movies/', views.MoivesAPIView.as_view()),
]