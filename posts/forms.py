from dataclasses import field
from logging import PlaceHolder
from turtle import numinput, title
from django import forms
from .models import Post

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'number', 'location', 
        'apply_link', 'tag', 'contact', 'duration']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px'}}),
            'title': forms.TextInput(attrs={'placeholder': '제목을 작성해주세요'}),
            'number': forms.TextInput(attrs={'placeholder': '직접 입력'}),
            'location': forms.TextInput(attrs={'placeholder': '직접 입력'}),
            'apply_link': forms.TextInput(attrs={'placeholder': '구글폼 링크를 입력해주세요'}),
            'contact': forms.Select(attrs={'placeholder': '온라인/오프라인/혼합'}),
            'duration': forms.Select(attrs={'placeholder': '번개/정기'})

        }