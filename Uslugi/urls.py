from django.conf import settings
from django.contrib import admin
from django.urls import path, include
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
    path('dannye/', views.dannye_view, name='dannye'),
    path('catalog/', views.catalog_view, name='catalog'),
]
if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)