from dataclasses import field
from pyexpat import model
from django import forms
from .models import Place
from django_summernote.widgets import SummernoteWidget

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'location', 'location_detail', 'category', 'opening_time', 'closing_time',
                'wifi', 'power_socket', 'rating', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '상호명을 입력해주세요'}),
            'location': forms.TextInput(attrs={'placeholder': '주소를 입력해주세요'}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px'}}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),  
            'closing_time': forms.TimeInput(attrs={'type': 'time'})  
        }



