from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# from restaurant.user.forms import UserLoginForm, UserCreationForm


from .forms import UserCreationForm, UserLoginForm


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
            form.save()
            return redirect('user:login')
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('menu:main')
