from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone', 'created_at']  # 添加 created_at 字段
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("不可用的用户名和密码")
            if not user.is_active:
                raise serializers.ValidationError("用户名已存在")
        else:
            raise serializers.ValidationError("必须有用户名和密码")

        data['user'] = user
        return data


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['username', 'sql_type', 'sql_address', 'sql_port', 'sql_login_name', 'sql_pwd', 'sql_name',
                  'created_at']


class PartialDatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['sql_name', 'sql_type', 'sql_address', 'sql_port', 'id']


class DatabaseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['id', 'sql_name']


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['created_at', 'search_sql_name', 'search_query']
