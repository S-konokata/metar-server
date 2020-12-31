from django import forms


class MetarAppForm(forms.Form):
    icao = forms.CharField(label='空港コード（RJ__）')
    search_date = forms.DateField(
        label='日付',
        widget=forms.DateInput(
            attrs={'class': 'flatpickr'}
        )
    )
