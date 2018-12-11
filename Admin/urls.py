from django.conf.urls import url

from Admin import views

urlpatterns = [
    url(r'^users/', views.AdminUsersAPIView.as_view()),
    url(r'^permissions/', views.PermissionsAPIView.as_view()),
]