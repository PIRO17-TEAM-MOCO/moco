from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('find-id/', views.find_id, name='find_id'),
    path('profile/<int:id>', views.profile_view, name='profile_view'),
    path('profile/edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('profile/add/<int:id>', views.profile_add, name='profile_add'),
    path('signout/', views.signout, name='signout'),
    path('change-pw/', views.change_pw, name='change_pw'),
    path('reset-pw/', views.reset_pw, name='reset_pw'),
    path('reset-pw/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_pw_done.html'),
         name='reset_pw_done'),
    path('reset-pw/confirm/<uidb64>/<token>/',
         views.CustomConfirmView.as_view(template_name='users/reset_pw_confirm.html'),
         name='reset_pw_confirm'),
    path('reset-pw/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_pw_complete.html'),
         name='reset_pw_complete'),
    path('likes/<int:tag>', views.likes, name="likes"),
    #path('social/signup/', views.social_error, name="social_error"),
    path('check/', views.social_check, name='social_check')
]