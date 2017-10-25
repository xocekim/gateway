from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^setup', views.setup, name='setup'),
    url(r'^$', views.index, name='index'),
    url(r'^bill/json', views.bill_json, name='bill_json'),
    url(r'^bill', views.bill, name='bill')
]