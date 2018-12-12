from rest_framework import serializers

from Cinema.models import CinemaUser, CinemaMovieOrder, Cinema


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


class CinemaMovieOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CinemaMovieOrder
        fields = ("c_user_id", "c_movie_id", "c_status", "c_price", "is_delete")


class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        fields = ("c_name", "c_address", "c_phone")
