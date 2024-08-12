from django.urls import path
from . import views
from django.contrib import admin
app_name = 'menu'
urlpatterns = [
    path('', views.main, name='main'),
    path('information/', views.information, name='information'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>', views.category, name='category'),
    path('dish/<int:dish_id>', views.dish, name='dish'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('starters/', views.starters, name='starters'),
    path('main_courses/', views.main_courses, name='main_courses'),
    path('soups/', views.soups, name='soups'),
    path('desserts/', views.desserts, name='desserts'),
    path('beverages/', views.beverages, name='beverages')
]


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Ресторан Istanbul'