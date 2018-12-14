import datetime

from django.db import models

from Cinema.models import PaiDang


class ViewerUser(models.Model):

    v_username = models.CharField(max_length=32, unique=True)
    v_password = models.CharField(max_length=256)

    def permission_set(self):
        return ViewerPermission.objects.filter(v_user_id=self.id)

    def has_permission(self, permission_name):
        permissions = self.permission_set()
        for permission in permissions:
            if Permission.objects.get(pk=permission.v_permission_id).p_name == permission_name:
                return True
        return False

    def check_password(self, password):
        return self.v_password == password


class Permission(models.Model):
    p_name = models.CharField(max_length=32, unique=True)


class ViewerPermission(models.Model):
    v_user_id = models.IntegerField(default=0)
    v_permission_id = models.IntegerField(default=0)


ORDERED_NOT_PAY = 0
ORDERED_PAYED = 1
ORDERED_CANCLE = 2


class ViewerOrder(models.Model):
    v_user = models.ForeignKey(ViewerUser)
    v_paidang = models.ForeignKey(PaiDang)
    v_expire = models.DateTimeField(default=datetime.datetime.now)
    v_price = models.FloatField(default=1)
    v_status = models.IntegerField(default=ORDERED_NOT_PAY)
    v_seats = models.CharField(max_length=256)

    # def set_expire(self):
    #     self.v_expire = datetime.datetime.now() + datetime.timedelta(minutes=15)