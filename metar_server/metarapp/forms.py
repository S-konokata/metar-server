from __future__ import annotations
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Metar


class MyLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class MetarAppForm(forms.Form):
    icao = forms.CharField(
        label='空港コード（RJ__）',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    search_date = forms.DateTimeField(
        input_formats=[r'%Y-%m-%d'],
        label='日付',
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control flatpickr'}
        )
    )
    metar_order = forms.ChoiceField(
        label='METAR並び順（時間）',
        choices=[
            ('asc', '昇順'),
            ('desc', '降順')
        ],
        widget=forms.RadioSelect()
    )

    def clean(self) -> dict[str, any]:
        cleaned_data = super().clean()
        cleaned_icao = cleaned_data.get('icao')
        if not re.search(Metar.STATION_ID_RE, cleaned_icao):
            raise forms.ValidationError('ICAO ID "RJ__"を入力してください')
        cleaned_search_date = cleaned_data.get('search_date')
        if not cleaned_search_date:
            raise forms.ValidationError('日付を入力してください')
        return cleaned_data


class GetMetarNowForm(forms.Form):
    airport = forms.MultipleChoiceField(
        label='Choose airport',
        choices=[],
        widget=forms.SelectMultiple(attrs={'size': 5, 'id': 'airport_select'})
    )

    def __init__(self, airport_list: list[str], *args, **kwargs) -> None:
        """Add airports to choices of this form.

        Other arguments are for super().__init__()

        Args:
            airport_list (list[str]): airport list from Airport model.
        """
        super().__init__(*args, **kwargs)
        self.fields['airport'].choices = [(id, id) for id in airport_list]
