from rest_framework import serializers
from user.models import User
from .models import Menu, Category, SumOrder



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


