from django.urls import path

from . import views

app_name = "likes"

urlpatterns = [
    path('add/<int:id>/<int:tag>', views.add, name="add"),
    path('delete/<int:id>/<int:tag>', views.delete, name="delete"),
]
