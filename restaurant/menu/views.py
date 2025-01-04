import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum, Case, When, Value, ExpressionWrapper, F, IntegerField, DecimalField
from django.shortcuts import render, redirect

from .models import Menu, Category, SumDish, SumOrder
from user.models import User


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
    bf = Menu.objects.filter(category_id_id__name_category='Завтраки')
    return render(request, 'menu/breakfast.html', context={'bf': bf })


def starters(request):
    st = Menu.objects.filter(category_id_id__name_category='Холодные закуски')
    return render(request, 'menu/starters.html', context={'st': st})

def main_courses(request):
    mc = Menu.objects.filter(category_id_id__name_category='Горячие блюда')
    return render(request, 'menu/main_courses.html', context={'mc': mc})

def soups(request):
    ss = Menu.objects.filter(category_id_id__name_category='Супы')
    return render(request, 'menu/soups.html', context={'ss': ss})

def desserts(request):
    ds = Menu.objects.filter(category_id_id__name_category='Десерты')
    return render(request, 'menu/desserts.html', context={'ds': ds})

def beverages(request):
    bs = Menu.objects.filter(category_id_id__name_category='Напитки')
    return render(request, 'menu/beverages.html', context={'bs': bs})

# def random_dish(request):
#     count = Menu.objects.all().values('id').count()
#     number = random.randint(1, count)
#     return redirect('menu:dish', dish_id=number)

def random_dish(request):
    count = Menu.objects.all().aggregate(Count('dish_name'))
    c = count.setdefault('dish_name__count')
    number = random.randint(1, c)
    return redirect('menu:dish', dish_id=number)
def top_5(request):
    top = SumDish.objects.values('menu_item_id').annotate(sum_by_dish=Sum('quantity')).order_by('-sum_by_dish')[:5]
    top = list(top)
    print(top)
    t = []
    for i in top:
        t.append(i['menu_item_id'])
    dishes = Menu.objects.filter(id__in=t)
    return render(request, 'menu/top_5.html', context={'dishes': dishes, 'top': top, 't': t})

def all_dishes(request):
    sort_by = request.GET.get('sort', 'pk')
    res = request.GET
    if sort_by not in ['dish_name', 'price']:
        sort_by = 'pk'
    result_all_dishes = Menu.objects.all().order_by(sort_by)
    return render(request, 'menu/all_dishes.html', context={'result_all_dishes': result_all_dishes, 'res': res})

# def all_orders(request):
#     sort_by = request.GET.get('sort', 'pk')
#     res = request.GET
#     if sort_by not in ['created_at_date', 'sum_order']:
#         sort_by = 'pk'
#     result_all_orders = SumOrder.objects.all().order_by(sort_by)
#     return render(request, 'menu/all_orders.html', context={'result_all_orders': result_all_orders, 'res': res})

def all_orders(request):
    ord = SumOrder.objects.values('sum_order', 'id', 'created_at_date').annotate(
        discount=Case(When(sum_order__gt=20000, then=Value(20)),
                  When(sum_order__gt=10000, then=Value(10)),
                  default=Value(0))).annotate(sum_order_with_discount=Case(
                    When(sum_order__gt=20000, then=(ExpressionWrapper(F('sum_order') - F('sum_order') * 0.2, IntegerField()))),
                        When(sum_order__gt=10000, then=(ExpressionWrapper(F('sum_order') - F('sum_order') * 0.1, IntegerField()))),
                        default=Value(0)))
    # ord = SumOrder.objects.values('sum_order').annotate(
    #     discount=Case(When(sum_order__gt=20000, then=Value(20)),
    #               When(sum_order__gt=10000, then=Value(10)),
    #               default=Value(0))).annotate(new_sum_order=F('sum_order') * Value(1 - (F('discount')) * 0.01))

    return render(request, 'menu/all_orders.html', context={'ord': ord})

def order(request, order_id):
    zakaz = SumDish.objects.filter(order_id=order_id).select_related('menu_item').select_related('category_id')
    return render(request, 'menu/order.html', context={'zakaz': zakaz})

def all_orders(request):
    sort_by = request.GET.get('sort', 'pk')
    if sort_by not in ['created_at_date', 'sum_order']:
        sort_by = 'pk'
    ord = SumOrder.objects.all().order_by(sort_by)
    paginator = Paginator(ord, 5)
    number_page = request.GET.get('page')
    try:
        page_obj = paginator.page(number_page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'menu/all_orders.html',
                  context={'page_obj': page_obj, 'sort_by':sort_by})


def analitics(request):
    return render(request, 'menu/analitics.html')

def top_5_by_sum(request):
    top = SumOrder.objects.values('user_id').annotate(sum_by_user=Sum('sum_order')).order_by('-sum_by_user')
    top = list(top)
    print(top)

    users = User.objects.values('username', 'phone_number', 'id')
    users = list(users)
    for m in top:
        for n in users:
            if m['user_id'] == n['id']:
                m['username'] = n['username']
                m['phone_number'] = n['phone_number']

    return render(request, 'menu/top_5_by_sum.html', context={'top': top})

def top_5_by_quantity(request):
    top = SumOrder.objects.values('user_id').annotate(quantity_by_user=Count('id'))
    top = list(top)
    print(top)
    t = []
    for i in top:
        t.append(i['user_id'])
    users = SumOrder.objects.filter(id__in=t)
    return render(request, 'menu/top_5_by_quantity.html', context={'users': users, 'top': top, 't': t})

def top_5_lentil_soup(request):
    # top = SumOrder.objects.select_related('id').values('user_id').annotate(quantity_by_user=Count('user_id')).filter(menu_item_id=4)
    # top = SumOrder.objects.select_related('user_id').aggregate(quantity_by_user=Count('user_id'))
    top = SumOrder.objects.select_related('id').values('user_id').annotate(quantity_by_user=Count('user_id'))
    top = list(top)
    print(top)
    t = []
    for i in top:
        t.append(i['user_id'])
    users = SumOrder.objects.filter(id__in=t)
    return render(request, 'menu/top_5_lentil_soup.html', context={ 'users': users, 'top': top, 't': t})
