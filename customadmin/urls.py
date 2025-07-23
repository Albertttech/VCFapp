# customadmin/urls.py
from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('view-vcf/<int:vcf_id>/', views.view_vcf_admin, name='view_vcf'),
    path('create-vcf/', views.create_vcf_admin, name='create_vcf'),
    path('all-vcf/', views.all_vcf_admin, name='all_vcf'),
    path('', views.dashboard_view, name='index'),  # This handles /admin/
]