from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('write-post/<int:id>', views.write_post, name="write-post"),
    path('write-place/<int:id>', views.write_place, name="write-place"),
    path('write-notice/<int:id>', views.write_notice, name="write-notice"),
    path('revise/<int:id>', views.revise, name="revise"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('recomment/<int:id>', views.recomment, name="recomment"),
]
