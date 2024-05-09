from django.db import models



class Menu(models.Model):
    dish_name = models.CharField(max_length=50)
    dish_description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.dish_name

class Category(models.Model):
    name_category = models.CharField(max_length=40)

    def __str__(self):
        return self.name_category




