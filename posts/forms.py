from dataclasses import field
from logging import PlaceHolder
from turtle import numinput
from django import forms
from .models import Post

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'number', 'location', 'apply_link', 'tag', 'contact', 'duration']
        widgets = {
            'content': SummernoteWidget(),
        }