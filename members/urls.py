from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('register/', views.member_register, name='register'),
    path('dashboard/', views.member_dashboard, name='dashboard'),
    path('vcf-tabs/', views.vcf_tabs, name='vcf_tabs'),
    path('subscribe-vcf/<int:vcf_id>/', views.subscribe_vcf, name='subscribe_vcf'),
    path('', views.member_login),  # Redirect root to login
]