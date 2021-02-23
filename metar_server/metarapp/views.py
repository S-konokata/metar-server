from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from django.http import HttpRequest
from datetime import timedelta
from .forms import MyLoginForm, MetarAppForm
from .models import Metar


@login_required(login_url='/metarapp/login')
def index(request: HttpRequest):
    params = {
        'user_name': request.user.username,
        'icao': '',
        'getdate': '',
        'form': MetarAppForm(),
        'outmetar': ''
    }
    if (request.method == 'POST'):
        form_post = MetarAppForm(request.POST)
        if not form_post.is_valid():
            params['form'] = form_post
            return render(request, 'metarapp/index.html', params)
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


def logout(request):
    return logout_then_login(request=request, login_url='/metarapp/login')


class Login(LoginView):
    form_class = MyLoginForm
    template_name = 'metarapp/login.html'
