# members/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import MemberRegisterForm, MemberLoginForm
from common.decorators import member_required


def member_register(request):
    # If already authenticated as member → go to dashboard
    if request.user.is_authenticated:
        if request.user.is_staff:
            # If staff, log them out before allowing member registration
            logout(request)
        else:
            return redirect('members:dashboard')

    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Ensure no staff flag
            user.save()
            login(request, user)
            return redirect('members:dashboard')
    else:
        form = MemberRegisterForm()
    return render(request, 'members/register.html', {'form': form})


def member_login(request):
    # If already logged in as NON-staff → redirect to dashboard
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('members:dashboard')

    # If staff is logged in → force logout first
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)

    error = None
    if request.method == 'POST':
        form = MemberLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                error = "Admins cannot log in here. Please use the admin portal."
            else:
                login(request, user)
                return redirect('members:dashboard')
        else:
            error = "Invalid credentials."
    else:
        form = MemberLoginForm()

    return render(request, 'members/login.html', {'form': form, 'error': error})


def member_logout(request):
    logout(request)
    return redirect('members:login')


@member_required
def member_dashboard(request):
    return render(request, 'members/dashboard.html')