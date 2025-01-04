from django.db import models

from user.models import User


class Menu(models.Model):
    dish_name = models.CharField(max_length=50)
    dish_description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.dish_name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

class Category(models.Model):
    name_category = models.CharField(max_length=40)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class SumOrder(models.Model):
    created_at_date = models.DateField(auto_now=True)
    created_at_time = models.TimeField(auto_now=True)
    sum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.created_at_date}'

class SumDish(models.Model):
    order = models.ForeignKey(SumOrder, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_sum = self.quantity * self.menu_item.price
        super().save(*args, **kwargs)
        self.update_sum_order()

    def delete(self, *args, **kwargs):
        order_sum = self.total_sum
        super().delete(*args, **kwargs)
        self.update_sum_order(-order_sum*2)


    def update_sum_order(self, adj=0):
        order = self.order
        current_sum = order.sum_order
        new_sum = current_sum + self.total_sum + adj
        order.sum_order = new_sum
        order.save()


    def __str__(self):
        return f'Заказ № {self.order.id}'


