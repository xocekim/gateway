manage.py startapp <module_name>

create directory module_name/static  
create directory module_name/templates  
create directory module_name/templates/module_name

create module_name/urls.py

    ```
	from django.conf import url
	from . import views
	
	urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^setup', views.setup, name='setup')
	]
	```

edit module_name/views.py

    ```
    from django.shortcuts import render, redirect
    from django.contrib.auth.decorators import login_required
    
    from .models import Credential, CredentialForm
	module_name = 'Module Name'
	module_location = '/module_name/'

	
	@login_required
	def index(request):
	    if Credential.objects.count() == 0:
            return redirect(setup)
		return render(request, 'module_name/index.html')

		
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
        return render(request, 'module_name/setup.html', {'form': form})		
	```

create module_name/templates/module_name/index.html

    ```
	{% extends 'gateway/base.html' %}
	{% block title %}Module Name{% endblock %}
	{% block navbar %}
		<a href="!#" class="breadcrumb">Module Name</a>
	{% endblock %}
	{% block content %}
		<h1>Module Name</h1>
	{% endblock %}
	```
	
create module_name/templates/module_name/setup.html

    ```
    {% extends 'gateway/base.html' %}
    
    {% block title %}Module Name Setup{% endblock %}
    
    {% block navbar %}
        <a href="/module_name" class="breadcrumb">Module Name</a>
        <a href="#" class="breadcrumb">Setup</a>
    {% endblock %}
    
    {% block content %}
        <form method="post" action="{% url 'setup' %}">
            {% csrf_token %}
            {{ form }}
            <input type="submit" value="Save" class="btn" />
        </form>
    {% endblock %}
    ```
    
edit module_name/models.py

    ```
    from django.db import models
    from django.forms import ModelForm
    
    
    class Credential(models.Model):
        username = models.CharField(max_length=100)
        password = models.CharField(max_length=100)
    
    class CredentialForm(ModelForm):
        class Meta:
            model = Credential
            fields = ['username', 'password']
     ```

edit module_name/admin.py

    ```
    from django.contrib import admin
    from .models import Credential
    
    admin.site.register(Credential)
    ```

edit gateway/settings.py

	```MY_MODULES = [..., 'module_name']```

edit gateway/urls.py

	```urlpatterns = [..., url(r'^soenergy/', include('soenergy.urls'))]```
