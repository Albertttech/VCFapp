# common/decorators.py
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect


def member_required(view_func):
    @login_required(login_url='/members/login/')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return HttpResponseForbidden("Staff users are not allowed in the member area.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @login_required(login_url='/admin/login/')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Only staff members can access this area.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view