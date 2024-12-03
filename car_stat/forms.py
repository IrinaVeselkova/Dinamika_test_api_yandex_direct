from django import forms
from .models import CarBrand, Region, QueryType

class QueryForm(forms.Form):
    #car_brand = forms.ModelChoiceField(queryset=CarBrand.objects.all())
    #region = forms.ModelChoiceField(queryset=Region.objects.all())
    #query_type = forms.ModelChoiceField(queryset=QueryType.objects.all())
    pass
