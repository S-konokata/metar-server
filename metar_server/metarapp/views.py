from django.shortcuts import render
from django.http import HttpResponse
from .forms import MetarAppForm


def index(request):
    params = {
        'icao': '',
        'getdate': '',
        'form': MetarAppForm()
    }
    if (request.method == 'POST'):
        params['icao'] = request.POST['icao']
        params['getdate'] = request.POST['search_date']
        params['form'] = MetarAppForm(request.POST)
    return render(request, 'metarapp/index.html', params)
