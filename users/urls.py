from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('find_id/', views.find_id, name='find_id'),
    path('profile/<int:id>', views.profile_view, name='profile_view'),
    path('profile/edit/<int:id>', views.profile_edit, name='profile_edit'),
]