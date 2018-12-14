from django.conf.urls import url

from Viewer import views

urlpatterns = [
    url(r'^users/', views.ViewerUSerAPIView.as_view()),
    url(r'^orders/', views.ViewerOrdersAPIView.as_view()),
    url(r'^seats/', views.SeatsAPIView.as_view()),
    url(r'^orders2/', views.voa2.as_view()),
    url(r'^tickettop/', views.TicketTopAPIView.as_view()),
]