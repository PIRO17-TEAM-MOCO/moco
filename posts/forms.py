from dataclasses import field
from logging import PlaceHolder
from turtle import numinput
from django import forms
from .models import Post

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'number', 'location', 'apply_link', 'tag', 'contacts', 'durations']
        widgets = {
            'content': SummernoteWidget(),
            'number': forms.NumberInput(attrs={'placeholder': '직접 입력'}),
            'location': forms.TextInput(attrs=('placeholder': '직접 입력')),
            'apply_link': forms.TextInput(attrs=('placeholder': '구글폼 링크를 입력해주세요')),
            'tag': forms.TextInput(attrs=('placeholder': '직접 입력')),
            'title': forms.TextInput(attrs=('placeholder': '제목을 작성해주세요')),
        }