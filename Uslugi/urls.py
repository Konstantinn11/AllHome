from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as v
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home_page"),
    path('register/', views.register_customer, name='register'),
    path('login/', v.LoginView.as_view(next_page='home_page'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('masters/', views.masters_view, name='masters'),
    path('masters/<int:pk>', views.master_detail_view, name='master_detail'),
    path('dannye/', views.dannye_view, name='dannye'),
    path('catalog/', views.catalog_view, name='catalog'),

    path('catalog/<slug:slug>', views.uslugi_view, name='uslugi_cat'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('zayavki/', views.zayavki_view, name='zayavki'),

    path('api/get_services_by_category/', views.get_services_by_category, name='get_services_by_category'),

    path('reports/virychka/', views.get_virychka, name='reports_virychka'),
    path('reports/masters/', views.get_masters, name='reports_masters'),
    path('reports/virychkamonth/', views.get_virychka_month, name='reports_virychka_month'),
    path('reports/masterssumma/', views.get_masters_summa, name='reports_masters_summa'),
]
if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)