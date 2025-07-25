# members/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MemberRegisterForm, MemberLoginForm
from common.decorators import member_required


def member_register(request):
    """
    Handles member registration
    - Logs out staff users if they try to register
    - Redirects already logged-in members to dashboard
    - Creates new member accounts with is_staff=False
    """
    # Handle already authenticated users
    if request.user.is_authenticated:
        if request.user.is_staff:
            logout(request)  # Staff users must logout first
        else:
            return redirect('members:dashboard')

    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set username as country code + mobile number
            user.username = f"{form.cleaned_data['country_code']}{form.cleaned_data['mobile_number']}"
            user.is_staff = False  # Ensure new users are not staff
            user.save()
            print(f"[REGISTER SUCCESS] Member created: {user.mobile_number}")
            login(request, user)
            return redirect('members:dashboard')
        else:
            print(f"[REGISTER FAIL] Errors: {form.errors}")
    else:
        form = MemberRegisterForm()
    
    return render(request, 'members/register.html', {'form': form})


def member_login(request):
    """
    Handles member login
    - Redirects already logged-in members
    - Forces logout if staff user is logged in
    - Validates credentials and checks user type
    """
    # Handle already authenticated users
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('members:dashboard')  # Members go to dashboard
        logout(request)  # Staff users must logout first

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

    return render(request, 'members/login.html', {
        'form': form,
        'error': error
    })


def member_logout(request):
    """Handles member logout and redirects to login page"""
    logout(request)
    return redirect('members:login')


@member_required
def member_dashboard(request):
    """Protected member dashboard view"""
    return render(request, 'members/dashboard.html')