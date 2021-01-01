from django import forms


class MetarAppForm(forms.Form):
    icao = forms.CharField(
        label='空港コード（RJ__）',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    search_date = forms.DateField(
        label='日付',
        widget=forms.DateInput(
            attrs={'class': 'form-control flatpickr'}
        )
    )
