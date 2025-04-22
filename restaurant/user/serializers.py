from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', )


class UserSumOrderSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    #Это определение поля user, которое ожидает целочисленное значение (например, идентификатор пользователя).
    # Это поле будет использоваться для хранения идентификатора пользователя,
    # к которому относится сумма заказов.
    sum_by_user = serializers.DecimalField(max_digits=10, decimal_places=2)