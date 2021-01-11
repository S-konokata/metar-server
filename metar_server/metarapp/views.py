from django.shortcuts import render
from django.http import HttpResponse
from datetime import timedelta
from .forms import MetarAppForm
from .models import Metar


def index(request):
    params = {
        'icao': '',
        'getdate': '',
        'form': MetarAppForm(),
        'outmetar': ''
    }
    if (request.method == 'POST'):
        form_post = MetarAppForm(request.POST)
        form_post.is_valid()
        # POST data is "YYYY-MM-DD" format (no time string).
        # Therefore, time of start_datetime is 0:00 (local timezone).
        start_datetime = form_post.cleaned_data['search_date']
        end_datetime = start_datetime + timedelta(hours=23, minutes=59)
        params['icao'] = request.POST['icao']
        params['getdate'] = request.POST['search_date']
        params['form'] = form_post
        metar_return = Metar.objects \
            .filter(
                station_id=request.POST['icao'],
                observation_time__range=(start_datetime, end_datetime),
            ) \
            .order_by('observation_time')
        if request.POST['metar_order'] == 'desc':
            params['outmetar'] = metar_return.reverse()
        else:
            params['outmetar'] = metar_return
    return render(request, 'metarapp/index.html', params)
