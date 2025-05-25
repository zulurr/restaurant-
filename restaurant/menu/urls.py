from django.urls import path, include
from . import views
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, CategoryViewSet, TopByPriceViewSet, TopByMainCoursesViewSet, SumOrderViewSet, \
    BreakfastsViewSet, SoupsViewSet, BeveragesViewSet, DessertsViewSet, StartersViewSet
from user.views import UserViewSet, UserSumOrderViewSet

router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'top_10_by_price', TopByPriceViewSet, basename='top_10_by_price' )
router.register(r'main_courses', TopByMainCoursesViewSet, basename='main_courses' )
router.register(r'sum_order', SumOrderViewSet, basename='sum_order' )
router.register(r'users', UserViewSet, basename='users' )
router.register(r'sum_by_user', UserSumOrderViewSet, basename='sum_by_user' )
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'breakfasts', BreakfastsViewSet, basename='breakfasts')
router.register(r'soups', SoupsViewSet, basename='soups')
router.register(r'beverages', BeveragesViewSet, basename='beverages')
router.register(r'desserts', DessertsViewSet, basename='desserts')
router.register(r'starters', StartersViewSet, basename='starters')

app_name = 'menu'
urlpatterns = [
    path('api/', include(router.urls)),

    path('api/auth/', views.AuthView.as_view(), name='auth'),
    path('api/updateuser/', views.UpdateUserView.as_view(), name='updateuser'),

    path('', views.main, name='main'),
    path('information/', views.information, name='information'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('dish/<int:dish_id>/', views.dish, name='dish'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('starters/', views.starters, name='starters'),
    path('main_courses/', views.main_courses, name='main_courses'),
    path('soups/', views.soups, name='soups'),
    path('desserts/', views.desserts, name='desserts'),
    path('beverages/', views.beverages, name='beverages'),
    path('random_dish/', views.random_dish, name='random_dish'),
    path('top-5/', views.top_5, name='top_5'),
    path('all_dishes/', views.all_dishes, name='all_dishes'),
    path('all_orders/', views.all_orders, name='all_orders'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('analitics/', views.analitics, name='analitics'),
    path('clients_by_sum/', views.clients_by_sum, name='clients_by_sum'),
    path('clients_by_quantity/', views.clients_by_quantity, name='clients_by_quantity'),
    path('clients_lentil_soup/', views.clients_lentil_soup, name='clients_lentil_soup'),
    path('cart/', views.cart_view, name='cart'),
    path('add_cart/<int:menu_id>', views.add_cart, name='add_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('add_item_in_cart/<int:menu_id>', views.add_item_in_cart, name='add_item_in_cart'),
    path('remove_item_from_cart/<int:menu_id>', views.remove_item_from_cart, name='remove_item_from_cart'),

]


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Ресторан Istanbul'