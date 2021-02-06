from __future__ import annotations
from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList


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
        return super().clean()


class GetMetarNowForm(forms.Form):
    airport_choices = []
    airport = forms.MultipleChoiceField(
        label='Choose airport',
        choices=airport_choices,
        widget=forms.SelectMultiple(attrs={'size': 5, 'id': 'airport_select'})
    )

    def __init__(self, airport_list: list[str]) -> None:
        """Add airports to choices of this form.

        Other arguments are for super().__init__()

        Args:
            airport_list (list[str]): airport list from Airport model.
        """
        self.airport_choices.extend(airport_list)
        super().__init__()
