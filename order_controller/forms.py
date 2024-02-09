from datetime import datetime, time
from django import forms


"""
Тут я хотів використати звичайний forms.SelectDateWidget але в ньому не було годин і хвилин. 
Тому код знизу це чисто ChatGPT
"""

class CustomDateTimeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.SelectDateWidget(attrs={'class': 'date-select'}),
            forms.Select(choices=[(str(i), str(i).zfill(2)) for i in range(24)], attrs={'class': 'hour-select'}),
            forms.Select(choices=[(str(i), str(i).zfill(2)) for i in range(60)], attrs={'class': 'minute-select'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            date_str = value.date().isoformat()
            time_str = value.time().strftime('%H:%M')
            return [date_str, value.hour, value.minute]
        return [None, None, None]

class CustomDateTimeField(forms.fields.MultiValueField):
    widget = CustomDateTimeWidget

    def __init__(self, *args, **kwargs):
        fields = [
            forms.DateField(),
            forms.IntegerField(min_value=0, max_value=23),
            forms.IntegerField(min_value=0, max_value=59),
        ]
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            date = data_list[0]
            hours = int(data_list[1]) if data_list[1] else 0
            minutes = int(data_list[2]) if data_list[2] else 0
            return datetime.combine(date, time(hours, minutes))
        return None


class OrderForm(forms.Form):
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name', max_length=100)
    start_date = CustomDateTimeField(label='Start Date/Time')
    end_date = CustomDateTimeField(label='End Date/Time')