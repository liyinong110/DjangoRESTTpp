from django.conf.urls import url

from Viewer import views

urlpatterns = [
    url(r'^users/', views.ViewerUSerAPIView.as_view()),
    url(r'^orders/', views.ViewerOrdersAPIView.as_view()),
]