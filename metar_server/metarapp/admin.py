from __future__ import annotations
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, URLPattern
from .forms import GetMetarNowForm
from .models import Airport, Metar
from .myfunction import airport_function, metar_function


@admin.register(Metar)
class MetarAdmin(admin.ModelAdmin):
    def get_urls(self) -> list[URLPattern]:
        urls = super().get_urls()
        my_urls = [
            path(
                'metar_manage_view',
                self.admin_site.admin_view(self.metar_manage_view),
                name='metar_manage'
            )
        ]
        return my_urls + urls

    def metar_manage_view(self, request):
        airport_metar_newest = airport_function.AirportMetarNewest()
        params = {
            'newest_datetimes': airport_metar_newest.newest_dict,
            'form': GetMetarNowForm(airport_metar_newest.airport_list),
            'get_metar_response': ''
        }
        if (request.method == 'POST'):
            fetch_airport: list[str] = request.POST.getlist('airport')
            get_metar = metar_function.MetarInput(fetch_airport)
            get_metar.fetch_and_save()
            metar_num_dict: dict[str: int] = {}
            for metar in get_metar.fetched_data:
                if metar.station_id in metar_num_dict:
                    metar_num_dict[metar.station_id] += 1
                else:
                    metar_num_dict[metar.station_id] = 1
            metar_all_num = 0
            for station in metar_num_dict:
                metar_all_num += metar_num_dict[station]
            fetched_time = get_metar.fetched_time.strftime(r"%Y %b %d %X %Z")
            params['get_metar_response'] = [
                'The METARs are fetched.',
                'The number of the METAR data in each airport:',
                str(metar_num_dict),
                f'The total number: {metar_all_num}',
                f'fetched datetime: {fetched_time}'
            ]
        return render(request, 'admin/metarapp/metar/metar_manage_view.html', params)


admin.site.register(Airport)
