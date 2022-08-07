from dataclasses import field
from django import forms
from .models import Place

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'location', 'category', 'opening_time', 'closing_time',
                'wifi', 'power_socket', 'rating', 'content']