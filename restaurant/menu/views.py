import random
from rest_framework import viewsets
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum, Case, When, Value, ExpressionWrapper, F, IntegerField, DecimalField, Max
from django.shortcuts import render, redirect

from .models import Menu, Category, SumDish, SumOrder

from .serializers import MenuSerializer, CategorySerializer, SumOrderSerializer

def main(request):
    queryset = SumOrder.objects.annotate(sum_by_user=Sum('sum_order')).order_by('-sum_by_user')
    return render(request, 'menu/main.html', context={'queryset':queryset})


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



def all_orders(request):
    ord = SumOrder.objects.values('sum_order', 'id', 'created_at_date').annotate(
        discount=Case(When(sum_order__gt=20000, then=Value(20)),
                  When(sum_order__gt=10000, then=Value(10)),
                  default=Value(0))).annotate(sum_order_with_discount=Case(
                    When(sum_order__gt=20000, then=(ExpressionWrapper(F('sum_order') - F('sum_order') * 0.2, IntegerField()))),
                        When(sum_order__gt=10000, then=(ExpressionWrapper(F('sum_order') - F('sum_order') * 0.1, IntegerField()))),
                        default=Value(0)))


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

def clients_by_sum(request):
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

    return render(request, 'menu/clients_by_sum.html', context={'top': top})

def clients_by_quantity(request):
    top = SumOrder.objects.values('user_id').annotate(quantity_by_user=Count('id')).order_by('-quantity_by_user')
    top = list(top)
    print(top)

    users = User.objects.values('username', 'phone_number', 'id')
    users = list(users)
    for m in top:
        for n in users:
            if m['user_id'] == n['id']:
                m['username'] = n['username']
                m['phone_number'] = n['phone_number']
    return render(request, 'menu/clients_by_quantity.html', context={'top': top})

def clients_lentil_soup(request):
    top = (SumDish.objects
           .select_related('order__user')
           .filter(menu_item=4)
           .values('order__user__id')  # Группировка по ID пользователя
           .annotate(total_quantity=Sum('quantity'))  # Суммирование поля quantity
           )
    top = list(top)


    new = (SumOrder.objects.prefetch_related('sumdish')
           .select_related('menu_item').filter(sumdish__menu_item=4)
           .values('user')
           .annotate(sum_soup=Sum('sumdish__quantity')))
    new = list(new)


    users = User.objects.values('username', 'phone_number', 'id')
    users = list(users)

    for m in top:
        for n in users:
            if m['order__user__id'] == n['id']:
                m['username'] = n['username']
                m['phone_number'] = n['phone_number']
    return render(request, 'menu/clients_lentil_soup.html', context={'top': top, 'new': new})


def add_cart(request, menu_id): # Добавляет элемент в корзину покупок.
# request: объект запроса, содержащий данные о текущем запросе пользователя.
# menu_id: идентификатор блюда, которое пользователь хочет добавить в корзину.


    cart = request.session.get('cart', {})
#  Получает текущую корзину из сессии пользователя (или создает пустую, если корзина не существует).
    if str(menu_id) in cart:
        cart[str(menu_id)]['count'] += 1
        # Проверяет, есть ли уже это блюдо в корзине (по его идентификатору).
        # Если блюдо уже в корзине, увеличивает его количество (count) на 1.
    else:
        item = Menu.objects.get(id=menu_id)
        cart[menu_id] = {
            'dish_name': item.dish_name,
            'price': str(item.price),
            'count': 1
        }
    request.session['cart'] = cart
# Если блюда нет в корзине, извлекает информацию о нем из базы данных (по menu_id) и
# добавляет его в корзину с начальным количеством 1.

    return redirect('menu:cart')





def cart_view(request): # Отображает содержимое корзины покупок пользователю.
    # request: объект запроса.
    cart = request.session.get('cart', {}) # Получает текущую корзину из сессии.
    total_price = 0
    # Инициализирует переменную total_price для подсчета общей стоимости всех товаров в корзине.

    for item in cart.values():
        total_price += float(item['price']) * item['count']
#  Проходит по всем элементам корзины и вычисляет общую стоимость,
    #  умножая цену каждого блюда на его количество (count).

    return render(request, 'menu/cart.html', context={'cart': cart, 'total_price': total_price})
# Возвращает HTML-шаблон (menu/cart.html), передавая в контекст данные о корзине и общей стоимости.


def clear_cart(request): # Очищает корзину покупок.
    if 'cart' in request.session: #  Проверяет, существует ли корзина в сессии пользователя.
        del request.session['cart'] # Если да, удаляет ее из сессии.

    return redirect('menu:all_dishes')

def add_item_in_cart(request, menu_id):
    cart = request.session.get('cart', {})

    if str(menu_id) in cart:
        cart[str(menu_id)]['count'] += 1


    request.session['cart'] = cart

    return redirect('menu:cart')

def remove_item_from_cart(request, menu_id):
    cart = request.session.get('cart', {})

    if str(menu_id) in cart:
        cart[str(menu_id)]['count'] -= 1
        if cart[str(menu_id)]['count'] < 1:
            del cart[str(menu_id)]



    request.session['cart'] = cart

    return redirect('menu:cart')

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SumOrderViewSet(viewsets.ModelViewSet):
    queryset = SumOrder.objects.all()
    serializer_class = SumOrderSerializer



class TopByPriceViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.order_by('-price')[:10]
    serializer_class = MenuSerializer

class TopByMainCoursesViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related('category_id').filter(category_id=3).order_by('-price')[:10]
    serializer_class = MenuSerializer

# class UserSumOrderViewSet(viewsets.ModelViewSet):
#     queryset = SumOrder.objects.values('user').annotate(sum_by_user=Sum('sum_order')).order_by('-sum_by_user')
#     serializer_class = UserSumOrderSerializer


class UserViewSet:
    pass