from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
   path('login/', views.login_view, name='login'),
   path('register/', views.register_view, name='register'),
   path('logout/', views.logout_view, name='logout'),
   path('profile/<int:user_id>', views.profile_view, name='profile'),
   path('profile_change/<int:user_id>', views.profile_change, name='profile_change'),
   path('profile_change_password/<int:user_id>', views.profile_change_password, name='profile_change_password'),
]
