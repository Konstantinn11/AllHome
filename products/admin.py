from django.contrib import admin
from django.apps import apps

app_config = apps.get_app_config('products')

NOT_REGISTERED_MODELS = []
for model in app_config.get_models():
    if not (model in NOT_REGISTERED_MODELS):
        admin.site.register(model)