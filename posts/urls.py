from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "posts"

urlpatterns = [
    path('', views.home, name="home"),
    path('write', views.write, name="write"),
    path('detail/<int:id>', views.detail, name="detail"),
    path('update/<int:id>', views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("close/<int:id>", views.close, name="close"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
