from django.shortcuts import redirect
from django.urls import reverse

class StaffRequiredMiddleware:
    """
    Restrict all non-admin URLs to logged-in staff users only.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_path = '/admin/'
        if not request.path.startswith(admin_path):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect(reverse('customadmin:login'))
        return self.get_response(request)
