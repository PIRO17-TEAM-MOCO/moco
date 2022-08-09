from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('find_id/', views.find_id, name='find_id'),
    path('profile/<int:id>', views.profile_view, name='profile_view'),
    path('profile/edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('signout/', views.signout, name='signout'),
]