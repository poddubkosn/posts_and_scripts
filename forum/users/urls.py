from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/', views.MyPasswordChange.as_view(),
         name='password_change_form'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='password_change_done'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='reset_complete'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),
         name='reset_confirm'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html'),
        name='password_reset_form',),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'), ]
