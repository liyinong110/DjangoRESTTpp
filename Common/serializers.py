from rest_framework import serializers

from Common.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("m_name", "m_duration", "m_leading_role", "m_director", "m_mode", "m_open_day")