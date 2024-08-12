from django.shortcuts import render

from .models import Menu, Category


def main(request):
    return render(request, 'menu/main.html')


def information(request):
    return render(request, 'menu/information.html')

def categories(request):
    categories = Category.objects.all().order_by('name_category')
    context = {'categories': categories}
    return render(request, 'menu/categories.html', context=context)

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    fruits = category.menu_set.all()
    context = {'category': category, 'fruits': fruits}
    return render(request, 'menu/category.html', context=context)

def dish(request, dish_id):
    dish = Menu.objects.get(id=dish_id)
    return render(request, 'menu/dish.html', context={'dish': dish})

def breakfast(request):
    return render(request, 'menu/breakfast.html')

def starters(request):
    return render(request, 'menu/starters.html')

def main_courses(request):
    return render(request, 'menu/main_courses.html')

def soups(request):
    return render(request, 'menu/soups.html')

def desserts(request):
    return render(request, 'menu/desserts.html')

def beverages(request):
    return render(request, 'menu/beverages.html')
