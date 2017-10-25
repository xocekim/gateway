# Gateway
This project is to create an easy to use and consistant looking portal for users to access their web accounts and associated details. 

## Modules
Currently working
- [Plusnet](https://plus.net)
- [So Energy](https://www.so.energy)

## Requirements
- django
- requests
- lxml
- cssselect

## Creating your own modules
There is a custom Django management script that creates the module directory and skeleton files required to being development on a new module
```shell
manage.py createmodule <module_name>
```
The files created and that you will need to customise to create your module are
- ```<module_name>/admin.py```
- ```<module_name>/models.py```
- ```<module_name>/urls.py```
- ```<module_name>/views.py```
- ```<module_name>/templates/<module_name>index.html```
- ```<module_name>/templates/<module_name>setup.html```

edit ```gateway/settings.py``` and enable the module

```python
MY_MODULES = [
    # .., 
    'module_name'
]
```

edit ```gateway/urls.py``` and enable the url routing for the module

```python
urlpatterns = [
    # ...,
    url(r'^module_name/', include('module_name.urls'))
]
```

create the necessary database migrations and apply them
```shell
manage.py makemigrations
manage.py migrate
```