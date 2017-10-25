import re

import lxml.html
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Credential, CredentialForm

module_name = 'Plusnet'
module_location = '/plusnet/'


@login_required
def index(request):
    if Credential.objects.count() == 0:
        return redirect(setup)
    return render(request, 'plusnet/index.html')


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
    return render(request, 'plusnet/setup.html', {'form': form})


@login_required
def bill(request):
    return render(request, 'plusnet/bill.html')


@login_required
def bill_json(request):
    plusnet_login_url = 'https://www.plus.net/index_nlp.html'
    session = requests.Session()
    cred = Credential.objects.get()
    form = {'username': cred.username, 'password': cred.password,
            'authentication_realm': 'portal.plus.net', 'x': '0', 'y': '0'}
    # we need to load some session cookies before we post login form
    session.get(plusnet_login_url)

    data = {}
    # do login and get next bill due date
    resp = session.post(plusnet_login_url, data=form)
    parser = lxml.html.fromstring(resp.content)
    try:
        due = parser.cssselect('div#notifyWhite')[0].text_content()
    except IndexError:
        return JsonResponse({'error': 'Invalid login credentials'})
    data['due'] = re.search(r'(\d+\/\d+\/\d+)', due).group(1)

    # get all historic transactions
    data['invoices'] = []
    resp = session.get('https://www.plus.net/my.html?action=view_transactions&s=0')
    parser = lxml.html.fromstring(resp.content)
    for row in parser.cssselect('table.table-grey tr')[2:]:
        invoice, value, balance, date, status, desc = row.cssselect('td')
        data['invoices'].append({'invoice': invoice.text_content().strip(),
                                 'value': value.text_content().strip(),
                                 'balance': balance.text_content().strip(),
                                 'date': date.text_content().strip(),
                                 'status': status.text_content().strip(),
                                 'desc': desc.text_content().strip()})

    # get broadband usage
    data['broadband'] = {}
    resp = session.get('https://www.plus.net/view_my_broadband_usage/index.php')
    parser = lxml.html.fromstring(resp.content)
    product, period = parser.cssselect('div.vmbuProductDetails p')
    data['broadband']['product'] = product.text.strip('- ')
    data['broadband']['period'] = period.text.strip()
    data['broadband']['usage'] = parser.cssselect('h4.usageAllowance')[0].text_content().strip()
    return JsonResponse(data)
