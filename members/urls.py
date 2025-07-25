from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('register/', views.member_register, name='register'),
    path('dashboard/', views.member_dashboard, name='dashboard'),
    path('', views.member_login),  # Redirect root to login
]