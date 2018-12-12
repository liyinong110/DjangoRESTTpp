from rest_framework import serializers

from Cinema.models import CinemaUser


class CinemaUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CinemaUser
        fields = ("c_username", "c_password")

    def create(self, validated_data):
        user = CinemaUser()
        c_username = validated_data.get("c_username")
        user.c_username = c_username
        c_password = validated_data.get("c_password")
        user.set_password(c_password)

        user.save()
        return user