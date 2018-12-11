from rest_framework import serializers

from Admin.models import AdminUser


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminUser
        fields = ("a_username", "a_password")

    def create(self, validated_data):

        adminUser = AdminUser()
        a_username = validated_data.get("a_username")
        adminUser.a_username = a_username
        a_password = validated_data.get("a_password")
        adminUser.set_password(a_password)

        adminUser.save()

        return adminUser