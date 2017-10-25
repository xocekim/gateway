from importlib import import_module

from django.conf import settings


def loaded_modules(request):
    modules = [import_module(f'{m}') for m in settings.MY_MODULES]
    return {'loaded_modules': modules}