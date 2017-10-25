from django.db import models
from django.forms import ModelForm


class Credential(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class CredentialForm(ModelForm):
    class Meta:
        model = Credential
        fields = ['username', 'password']