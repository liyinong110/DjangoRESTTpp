from django.conf.urls import url

from Admin import views

urlpatterns = [
    url(r'^users/', views.AdminUsersAPIView.as_view()),
]