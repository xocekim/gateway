import os
import shutil

from django.core.management.base import BaseCommand, CommandError


FILE_URLS_PY = """from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setup', views.setup, name='setup')
]
"""

FILE_VIEWS_PY = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Credential, CredentialForm

module_name = '{{MODULE_NAME}}'
module_location = '/{{MODULE_NAME}}/'


@login_required
def index(request):
    if Credential.objects.count() == 0:
        return redirect(setup)
    return render(request, '{{MODULE_NAME}}/index.html')

    
@login_required
def setup(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            Credential.objects.all().delete()
            form.save()
            return redirect(index)
    else:
        if Credential.objects.count() > 0:
            form = CredentialForm(instance=Credential.objects.get())
        else:
            form = CredentialForm()
    return render(request, '{{MODULE_NAME}}/setup.html', {'form': form})
"""

FILE_INDEX_HTML = """{% extends 'gateway/base.html' %}
{% block title %}{{MODULE_NAME}}{% endblock %}
{% block navbar %}
    <a href="!#" class="breadcrumb">{{MODULE_NAME}}</a>
{% endblock %}
{% block content %}
    <h1>{{MODULE_NAME}}</h1>
{% endblock %}
"""

FILE_SETUP_HTML = """{% extends 'gateway/base.html' %}

{% block title %}{{MODULE_NAME}} Setup{% endblock %}

{% block navbar %}
    <a href="/{{MODULE_NAME}}" class="breadcrumb">{{MODULE_NAME}}</a>
    <a href="#" class="breadcrumb">Setup</a>
{% endblock %}

{% block content %}
    <form method="post" action="{% url 'setup' %}">
        {% csrf_token %}
        {{ form }}
        <input type="submit" value="Save" class="btn" />
    </form>
{% endblock %}
"""

FILE_MODELS_PY = """from django.db import models
from django.forms import ModelForm


class Credential(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class CredentialForm(ModelForm):
    class Meta:
        model = Credential
        fields = ['username', 'password']
"""

FILE_ADMIN_PY = """from django.contrib import admin
from .models import Credential

admin.site.register(Credential)
"""

class Command(BaseCommand):
    help = 'Creates a new gateway module for development'

    def add_arguments(self, parser):
        parser.add_argument('module_name', type=str)

    def handle(self, *args, **options):
        if os.path.exists(options['module_name']):
            answer = input('module already exists, continue? [y/n]').lower()
            if answer == 'y':
                answer = input('THIS WILL DELETE EVERYTHING IN THAT DIRECTORY, ARE YOU SURE? [y/n]').lower()
                if answer == 'y':
                    shutil.rmtree(options['module_name'])
                else:
                    return
            else:
                return

        os.makedirs('%s/templates/%s' % (options['module_name'], options['module_name']))
        os.makedirs('%s/static' % options['module_name'])

        with open('%s/urls.py' % (options['module_name'], ), 'w') as f:
            f.write(FILE_URLS_PY.replace('{{MODULE_NAME}}', options['module_name']))

        with open('%s/views.py' % (options['module_name'], ), 'w') as f:
            f.write(FILE_VIEWS_PY.replace('{{MODULE_NAME}}', options['module_name']))

        with open('%s/templates/%s/index.html' % (options['module_name'], options['module_name']), 'w') as f:
            f.write(FILE_INDEX_HTML.replace('{{MODULE_NAME}}', options['module_name']))

        with open('%s/templates/%s/setup.html' % (options['module_name'], options['module_name']), 'w') as f:
            f.write(FILE_SETUP_HTML.replace('{{MODULE_NAME}}', options['module_name']))

        with open('%s/models.py' % (options['module_name'], ), 'w') as f:
            f.write(FILE_MODELS_PY.replace('{{MODULE_NAME}}', options['module_name']))

        with open('%s/admin.py' % (options['module_name'], ), 'w') as f:
            f.write(FILE_ADMIN_PY.replace('{{MODULE_NAME}}', options['module_name']))

        self.stdout.write('module created %s' % options['module_name'])
