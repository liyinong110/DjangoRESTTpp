from rest_framework import serializers

from Viewer.models import ViewerUser, ViewerOrder


class ViewerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewerUser
        fields = ("v_username", "v_password")


class ViewerOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewerOrder
        fields = ("v_user_id", "v_paidang_id", "v_expire", "v_price", "v_status", "v_seats")