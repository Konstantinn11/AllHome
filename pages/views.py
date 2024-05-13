from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import logout, authenticate
from django.shortcuts import render

from django.db.models import Q
from products.models import Usluga
from products.forms import ProductCommentForm

import json


def home_view(request):
    return render(request, "home.html")


def dannye_view(request):
    return render(request, "dannye.html")


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('home_page')  # перенаправьте пользователя на нужную страницу
    return response


def contacts_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        username = request.user.username

        Contact.objects.create(
            username=username,
            message=message
        )

    return render(request, "contacts.html")


def masters_view(request):
    query = request.GET.get('masters_search')

    if query:
        q_obj = Q()
        words = [word for word in query.split() if len(word) > 2]
        for word in words:
            q_obj |= Q(first_name=word)
            q_obj |= Q(last_name=query)

        q_obj &= Q(employer_position__title='Мастер') 
        masters = Employer.objects.filter(q_obj)
    else:
        masters = Employer.objects.filter(employer_position__title='Мастер')

    response = {
        'masters': masters
    }

    return render(request, "masters.html", response)


def master_detail_view(request, pk):

    master = Employer.objects.get(pk=pk)
    otzovy = Comment.objects.filter(zayavka__employer__pk=pk)

    response = {
        'master': master,
        'otzovy': otzovy
    }
    return render(request, "otzovy.html", response)


def catalog_view(request):
    query = request.GET.get('service_search')

    if query:
        items = Usluga.objects.filter(title__icontains=query)
    else:
        items = UslugaCategory.objects.all()
       
    response = {
        'items': items           
    }

    if str(request.get_full_path())[:24] == '/catalog/?service_search':
        response.update({'search': 1})

    return render(request, "catalog.html", response)


def uslugi_view(request, slug):
    items = Usluga.objects.filter(category__slug=slug)
    response = {
        'items': items
    }
    return render(request, "uslugi_list.html", response)


def profile(request, pk):
    def only(instanse):
        return instanse.only(
            'number', 'date_document', 'address',
            'description', 'customer', 'employer'
        )
    
    try:
        user = Employer.objects.get(pk=pk)
    except:
        user = Customer.objects.get(pk=pk)

    # если заказчик
    if user.__class__ == Customer:
        orders = only(Zayavka.objects.filter(customer__pk=pk).order_by('-number'))
        title_on_page = f'{user.first_name} {user.last_name}, ваши заявки'
        current_user = 'customer'
    # если мастер
    elif user.employer_position.pk == 1:
        orders = only(Zayavka.objects.filter(employer__pk=pk).order_by('-number'))
        title_on_page = f'{user.last_name} {user.first_name}, ваши выполненые и текущие заявки'
        current_user = 'master'
    # если менеджер    
    elif user.employer_position.pk == 2:
        orders = only(Zayavka.objects.filter(stateozayvkas__status__title='На рассмотрении'))
        title_on_page = f'{user.last_name} {user.first_name}, все заявки на рассмотрении'
        current_user = 'manager'
    # если директор
    elif user.employer_position.pk == 4:
        orders = only(Zayavka.objects.filter(stateozayvkas__status__title='Выполнена').order_by('-number'))
        title_on_page = f'{user.last_name} {user.first_name}, все выполненные заявки'
        current_user = 'direktor'

    if request.method == 'POST':
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.update_or_create(
                user=form.cleaned_data['user'],
                zayavka=form.cleaned_data['zayavka'],
                defaults={'text': form.cleaned_data['text']}
            )
        else:
            pass
    else:
        form = ProductCommentForm()

    response = {
        'orders': orders,
        'form': form,
        'zayavki_customer': Zayavka.objects.filter(customer__pk=pk),
        'current_user': current_user,
        'title_on_page': title_on_page
    }
    return render(request, "profile.html", response)


def zayavki_view(request):

    if request.method == 'POST':
        uslugi = Usluga.objects.all()
        masters = Employer.objects.all()
        data = json.loads(request.body)
        print(data)
        positions = []
        positions_and_prices = ''
        total_price = 0

        # получаем данные из формы
        for category in data['categories']:
            for service in data['categories'][category]:
                position = Position_Price.objects.get(pk=service[8:])
                position_price = position.cost_product
                quantity = int(data['categories'][category][service])
                positions_and_prices += f'{str(position.usluga.title)}\t x {quantity}\n'
                total_price += position_price * quantity
                positions.append(
                    Position_Price.objects.get(pk=service[8:])
                )

        # заполнить номер заявки
        try:
            number = str(int(Zayavka.objects.latest('pk').number) + 1)
        except:
            number = '0'
        
        number = f'{number.rjust(4, "0")}'

        # параметры для создания модели заявки
        zayvka = {
            'number': number,
            'date_document': data['date_document'],
            'address': data['address'],
            'description': data['comment'],
            'customer': Customer.objects.get(pk=request.user.pk),
            'employer': Employer.objects.get(pk=data['master'])
        }

        # создаем новую заявку
        new_zayavka = Zayavka.objects.create(**zayvka)
        new_zayavka.position.add(*positions)
        new_zayavka.total_price = total_price
        new_zayavka.positions_and_prices = positions_and_prices
        new_zayavka.save()

    else:       
        uslugi = Usluga.objects.filter(category=1)
        masters = Employer.objects.all()

    response = {
        'cats': UslugaCategory.objects.all(),
        'uslugi': uslugi,
        'masters': masters
    }

    return render(request, "zayavka.html", response)


def get_services_by_category(request):
    if request.method == 'GET':
        category = UslugaCategory.objects.get(pk=request.GET.get('category_id'))
        context = {
            'uslugi': Usluga.objects.filter(category=category),
            'masters': Employer.objects.filter(category=category)
        }
        return render(request, 'services_form_part.html', context)
