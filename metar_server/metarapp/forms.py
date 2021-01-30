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

    def __init__(self, airport_list: list[str], data: Optional[Mapping[str, Any]],
                 files: Optional[Mapping[str, Any]], auto_id: Optional[Union[bool, str]], prefix: Optional[str],
                 initial: Optional[Mapping[str, Any]], error_class: Type[ErrorList], label_suffix: Optional[str],
                 empty_permitted: bool, field_order: Optional[Any], use_required_attribute: Optional[bool],
                 renderer: Any) -> None:
        """Add airports to choices of this form.

        Other arguments are for super().__init__()

        Args:
            airport_list (list[str]): airport list from Airport model.
        """
        self.airport_choices.extend(airport_list)
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial,
                         error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted,
                         field_order=field_order, use_required_attribute=use_required_attribute, renderer=renderer)
