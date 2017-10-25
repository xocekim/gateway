from django.shortcuts import render
from django.contrib.auth.decorators import login_required


module_name = 'Twitter'
module_location = '/twitter/'


@login_required
def index(request):
    return render(request, 'twitter/index.html')