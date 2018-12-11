from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class AdminUser(models.Model):

    a_username = models.CharField(max_length=16, unique=True)
    a_password = models.CharField(max_length=256)

    is_delete = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)

    def set_password(self, password):
        self.a_password = make_password(password)

    def check_admin_password(self, password):
        return check_password(password, self.a_password)


class Permission(models.Model):
    p_name = models.CharField(max_length=32, unique=True)
    p_users = models.ManyToManyField(AdminUser)