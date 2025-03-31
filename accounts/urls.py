from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('set-new-password/<str:email>/<str:otp>/', views.set_new_password, name='set_new_password'),
]
