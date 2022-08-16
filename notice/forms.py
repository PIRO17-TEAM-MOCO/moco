from dataclasses import field
from django import forms
from .models import Notice
from django_summernote.widgets import SummernoteWidget

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력해주세요'}),
            'content': SummernoteWidget(),
        }