from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from products.models import *
from django.apps import apps

from products.models import Customer


class EmployerCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'otchestvo',
                                      'email', 'phone_number', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': 
                    ('date_of_employment', 'date_of_dismissal',
                    'employer_position', 'category')
                    })
    )


class CustomerCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'otchestvo',
                                      'email', 'phone_number', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )


@admin.register(Employer)
class AdvertAdmin(EmployerCustomAdmin):
    ...


@admin.register(Customer)
class AdvertAdmin(CustomerCustomAdmin):
    ...
    

admin.site.register(EmployerPosition)
admin.site.register(ZayavkaState)
admin.site.register(DogovorState)
admin.site.register(Price)
admin.site.register(Position_Price)
admin.site.register(Zayavka)
admin.site.register(UslugaCategory)
admin.site.register(Usluga)
admin.site.register(Comment)
admin.site.register(Dogovor)
admin.site.register(StateofDogovor)
admin.site.register(StateofZayavka)
admin.site.register(Contact)
admin.site.register(Act)
admin.site.register(Position_Act)


# app_config = apps.get_app_config('products')

# NOT_REGISTERED_MODELS = []
# for model in app_config.get_models():
#     if not (model in NOT_REGISTERED_MODELS):
#         admin.site.register(model)