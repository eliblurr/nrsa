from django import forms


class geo_data(forms.Form):
    date_from = forms.CharField()
    date_to = forms.CharField()
    region = forms.CharField()


class chart_data(forms.Form):
    date_from = forms.CharField()
    date_to = forms.CharField()
    region = forms.CharField()
    category = forms.CharField()
    specific = forms.CharField()


class time_series(forms.Form):
    option = forms.CharField()