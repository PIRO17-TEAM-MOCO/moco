from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('write/<int:id>', views.write, name="write"),
]
