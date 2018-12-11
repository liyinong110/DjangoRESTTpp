from rest_framework import serializers

from Admin.models import AdminUser, Permission


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
        is_super = validated_data.get("is_super")
        adminUser.is_super = is_super

        adminUser.save()

        return adminUser


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ("p_name", )