from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('write/<int:id>', views.write, name="write"),
    path('revise/<int:id>', views.revise, name="revise"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('recomment/<int:id>', views.recomment, name="recomment"),
]
