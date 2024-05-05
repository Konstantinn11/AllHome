from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import logout
from django.shortcuts import render


def home_view(request, *args, **kwargs):
    print(*args, **kwargs)

    return render(request, "home.html")

def dannye_view(request, *args, **kwargs):
    print(*args, **kwargs)

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


def contacts_view(request, *args, **kwargs):
    print(*args, **kwargs)
    return render(request, "contacts.html")


def masters_view(request, *args, **kwargs):
    print(*args, **kwargs)
    masters = Employer.objects.all()
    response = {
        'masters': masters
    }
    return render(request, "masters.html", response)

def catalog_view(request, *args, **kwargs):
    print(*args, **kwargs)
    items = UslugaCategory.objects.all()
    response = {
        'items': items
    }
    return render(request, "catalog.html", response)