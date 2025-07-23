import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .forms import VCFFileForm
from vcfviewer.models import VCFFile
from common.decorators import admin_required


# Add logger
logger = logging.getLogger(__name__)

# Admin login view
def login_view(request):
    logger.info(f"[LOGIN VIEW] Path: {request.path}")
    logger.info(f"[LOGIN VIEW] User authenticated: {request.user.is_authenticated}")
    
    if request.user.is_authenticated:
        logger.info(f"[LOGIN VIEW] User is_staff: {request.user.is_staff}")
    else:
        logger.info("[LOGIN VIEW] User is Anonymous")

    # If already logged in and is staff → go to dashboard
    if request.user.is_authenticated:
        if request.user.is_staff:
            logger.info("[LOGIN VIEW] Redirecting staff user to dashboard")
            return redirect('customadmin:dashboard')
        else:
            logger.info("[LOGIN VIEW] Non-staff user logged in → logging out + flushing session")
            logout(request)
            request.session.flush()  # Clear session
            logger.info("[LOGIN VIEW] Session flushed")

    # Now show login form
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                logger.info(f"[LOGIN VIEW] Staff login success: {username}")
                return redirect('customadmin:dashboard')
            else:
                error = "Only staff members can access this area."
                logger.info(f"[LOGIN VIEW] Non-staff login attempt: {username}")
        else:
            error = "Invalid login credentials."
            logger.info(f"[LOGIN VIEW] Failed login attempt: {username}")

    logger.info("[LOGIN VIEW] Rendering admin_login.html")
    return render(request, 'customadmin/admin_login.html', {'error': error})

@admin_required
def dashboard_view(request):
    return render(request, 'customadmin/dashboard.html')


# List all VCF files
@admin_required
def all_vcf_admin(request):
    vcfs = VCFFile.objects.all()
    for vcf in vcfs:
        vcf.current_count = vcf.contacts.count()
        vcf.progress = int((vcf.current_count / vcf.max_contacts) * 100) if vcf.max_contacts else 0
    return render(request, 'customadmin/all_vcf.html', {'vcfs': vcfs})


# View single VCF file
@admin_required
def view_vcf_admin(request, vcf_id):
    vcf = VCFFile.objects.get(id=vcf_id)
    contacts = vcf.contacts.all()
    current_count = contacts.count()
    progress = int((current_count / vcf.max_contacts) * 100) if vcf.max_contacts else 0
    return render(request, 'customadmin/view_vcf.html', {
        'vcf': vcf,
        'contacts': contacts,
        'current_count': current_count,
        'progress': progress,
    })


# Create VCF file
@admin_required
def create_vcf_admin(request):
    if request.method == 'POST':
        form = VCFFileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customadmin:dashboard')
    else:
        form = VCFFileForm()
    return render(request, 'customadmin/create_vcf.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('customadmin:login')