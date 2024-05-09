
from django import forms
from .models import Menu, Category

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['dish_name', 'dish_description', 'price', 'category_id']
        labels = {'dish_name': 'Название блюда', 'dish_description': 'Описание блюда',
                  'price': 'Цена', 'category_id': 'Категория'}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name_category']
        labels = {'name_category': 'Название категории'}