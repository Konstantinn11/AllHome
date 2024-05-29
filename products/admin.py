from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from products.models import *
from django.apps import apps

from products.models import Customer


class EmployerCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'otchestvo',
                                      'email', 'phone_number', 'image', 'soglasie')}),
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
                                      'email', 'phone_number', 'birth_date', 'soglasie')}),
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
# admin.site.register(Position_Price)
# admin.site.register(Price)
class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Прайс-лист', {
            'fields': [
                ('price_list'),
            ],
        }),
        ('Позиция прайс-листа и стоимость', {
            'fields': [
                ('usluga', 'cost_product'),
            ],
        })
    ]
admin.site.register(Position_Price, PositionAdmin)
class PositionPriceInline(admin.TabularInline):
    model = Position_Price
class PriceAdmin(admin.ModelAdmin):
    inlines = [PositionPriceInline]
admin.site.register(Price, PriceAdmin)

# admin.site.register(Zayavka)
class ZayavkaAdmin(admin.ModelAdmin):
    list_display = ('number', 'date_document', 'customer')
    list_filter = ('date_document', 'employer')
    change_form_template = "admin/change_form.html"  # Here

    actions = ['_generate_a_dogovor']

    def _generate_a_dogovor(self, request, queryset):
        pass

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['generate_a_dogovor'] = True  # Here

        return super().changeform_view(request, object_id, form_url, extra_context)
admin.site.register(Zayavka, ZayavkaAdmin)
admin.site.register(UslugaCategory)
admin.site.register(Usluga)
admin.site.register(Comment)
admin.site.register(Dogovor)
admin.site.register(StateofDogovor)
admin.site.register(StateofZayavka)
admin.site.register(Contact)
admin.site.register(Act)
admin.site.register(Position_Act)
admin.site.register(Pretensia)
admin.site.register(Position_Pretensia)
admin.site.register(StateofPretensia)
admin.site.register(PretensiaState)


# app_config = apps.get_app_config('products')

# NOT_REGISTERED_MODELS = []
# for model in app_config.get_models():
#     if not (model in NOT_REGISTERED_MODELS):
#         admin.site.register(model)