from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from rest_framework import viewsets

# from restaurant.user.forms import UserLoginForm, UserCreationForm


from .forms import UserCreationForm, UserLoginForm, UserProfileChangeForm, CustomPasswordChangeForm
from .models import User
from user.serializers import UserSerializer, UserSumOrderSerializer
from menu.models import SumOrder


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu:main')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user:login')
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('menu:main')

def profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user/profile.html', {'user': user})

def profile_change(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method != 'POST':
        form = UserProfileChangeForm()
        form.fields['username'].initial = user.username
        form.fields['phone_number'].initial = user.phone_number
        form.fields['email'].initial = user.email
    else:
        form = UserProfileChangeForm(data=request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.phone_number = form.cleaned_data['phone_number']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('user:profile', user_id=user_id)
    return render(request, 'user/profile_change.html', {'form': form})

def profile_change_password(request, user_id):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user:profile', user_id=user_id)
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'user/profile_change_password.html', {'form': form})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSumOrderViewSet(viewsets.ModelViewSet):
    queryset = SumOrder.objects.values('user').annotate(sum_by_user=Sum('sum_order')).order_by('-sum_by_user')
    serializer_class = UserSumOrderSerializer


