from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "posts"

urlpatterns = [
    # post
    path('', views.home, name="home"),
    path('write', views.write, name="write"),
    path('detail/<int:id>', views.detail, name="detail"),
    path('update/<int:id>', views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("close/<int:id>", views.close, name="close"),
    # post-review
    path('review', views.review_home, name="review_home"),
    path('review/write/<int:id>', views.review_write, name="review_write"),
    path('review/revise/<int:id>', views.review_revise, name="review_revise"),
    path('review/delete/<int:id>', views.review_delete, name="review_delete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
