import re

import lxml.html
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Credential, CredentialForm

module_name = 'So Energy'
module_location = '/soenergy/'


@login_required
def index(request):
    if Credential.objects.count() == 0:
        return redirect(setup)
    return render(request, 'soenergy/index.html')


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
    return render(request, 'soenergy/setup.html', {'form': form})


@login_required
def bill(request):
    return render(request, 'soenergy/bill.html')


@login_required
def bill_json(request):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    soenergy_login_url = 'https://www.so.energy/users/sign_in'
    session = requests.Session()

    resp = session.get(soenergy_login_url, headers=headers)
    parser = lxml.html.fromstring(resp.content)
    token = parser.cssselect('meta[name=csrf-token]')[0].attrib['content']
    cred = Credential.objects.get()
    form = {'utf8': True, 'user[email]': cred.username, 'user[password]': cred.password,
            'authenticity_token': token}
    data = {}

    resp = session.post(soenergy_login_url, data=form, headers=headers)
    parser = lxml.html.fromstring(resp.content)
    data['credit'] = re.search(r'([\d\.]+)', parser.cssselect('span.cr')[0].getparent().text_content()).group(1)

    resp = session.get('https://www.so.energy/accounts/payments', headers=headers)
    parser = lxml.html.fromstring(resp.content)
    next_amount = parser.cssselect('p.size-big-money')[0]
    data['next_amount'] = re.search(r'([\d\.]+)', next_amount.text_content()).group(1)
    data['due'] = next_amount.getparent().text_content().split('on ')[-1].split('\n')[0]
    return JsonResponse(data)
