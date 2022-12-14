from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    path('', views.home, name='home'),
    path('write/', views.write, name='write'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    # 맨 아래에 넣어주세요
    path('<str:category>/', views.home, name='home'),
]