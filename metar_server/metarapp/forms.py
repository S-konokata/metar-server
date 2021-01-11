from __future__ import annotations
from django import forms


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
