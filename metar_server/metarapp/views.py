from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'metarapp/index.html')


def form(request):
    getIcao = request.POST['icao']
    getDate = request.POST['getdate']
    params = {
        'icao': getIcao,
        'getdate': getDate
    }
    return render(request, 'metarapp/index.html', params)
    