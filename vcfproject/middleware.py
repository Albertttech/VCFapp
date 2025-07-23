from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Member paths that should be accessible without staff status
        member_paths = [
            reverse('members:login'),
            reverse('members:logout'),
            reverse('members:register'),
        ]

        # Allow access to member paths
        if any(request.path.startswith(path) for path in member_paths):
            return self.get_response(request)

        # Allow access to static files
        if request.path.startswith('/static/'):
            return self.get_response(request)

        # For admin paths (/admin/), require staff status
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect(settings.ADMIN_LOGIN_URL)

        return self.get_response(request)
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for static files
        if request.path.startswith('/static/'):
            return self.get_response(request)
            
        # Skip middleware for admin login/logout
        if request.path in [reverse('customadmin:login'), reverse('customadmin:logout')]:
            return self.get_response(request)
            
        # For admin paths, require staff status
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('customadmin:login')
                
        return self.get_response(request)