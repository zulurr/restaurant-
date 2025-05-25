from rest_framework import serializers
from user.models import User
from .models import Menu, Category, SumOrder
from django.contrib.auth import authenticate



class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('dish_name', 'dish_description', 'price', 'image', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name_category', )


class SumOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SumOrder
        fields = ('user', 'sum_order')

class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['phone_number'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Неверные учетные данные!')
        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']
    #
    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         if value:
    #             setattr(instance, attr, value)
    #     instance.save()
    #     return instance


