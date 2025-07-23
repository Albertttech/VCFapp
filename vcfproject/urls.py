# vcfproject/urls.py
from django.contrib import admin
from django.urls import path, include

# main urls.py
urlpatterns = [
    path('members/', include('members.urls')),
    path('admin/', admin.site.urls),  # Built-in Django admin if used
    path('customadmin/', include('customadmin.urls')),
]
