import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from .forms import VCFFileForm
from vcfviewer.models import VCFFile
from common.decorators import admin_required

# Initialize logger
logger = logging.getLogger(__name__)

def login_view(request):
    """
    Handle admin authentication and redirects
    """
    # Log request details
    logger.info(f"Admin login attempt - Path: {request.path}, Authenticated: {request.user.is_authenticated}")
    
    # Redirect if already logged in as staff
    if request.user.is_authenticated:
        if request.user.is_staff:
            logger.info(f"Staff user {request.user.username} already authenticated, redirecting to dashboard")
            return redirect('customadmin:dashboard')
        else:
            logger.info("Non-staff user logged in - forcing logout")
            logout(request)
            request.session.flush()
            return redirect('customadmin:login')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                logger.info(f"Successful admin login for {username}")
                return redirect('customadmin:dashboard')
            else:
                error = "Only staff members can access this area."
                logger.warning(f"Non-staff login attempt: {username}")
        else:
            error = "Invalid login credentials."
            logger.warning(f"Failed login attempt for username: {username}")

    return render(request, 'customadmin/admin_login.html', {'error': error})

@admin_required
def dashboard_view(request):
    """Admin dashboard view"""
    return render(request, 'customadmin/dashboard.html')

@admin_required
def all_vcf_admin(request):
    """List all VCF files with progress data"""
    vcfs = VCFFile.objects.all()
    for vcf in vcfs:
        vcf.current_count = vcf.contacts.count()
        vcf.progress = int((vcf.current_count / vcf.max_contacts) * 100) if vcf.max_contacts else 0
    return render(request, 'customadmin/all_vcf.html', {'vcfs': vcfs})

@admin_required
def view_vcf_admin(request, vcf_id):
    """View details of a specific VCF file"""
    try:
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
    except VCFFile.DoesNotExist:
        logger.error(f"VCF file with id {vcf_id} not found")
        return HttpResponseForbidden("VCF file not found")

@admin_required
def create_vcf_admin(request):
    """Handle VCF file creation"""
    if request.method == 'POST':
        form = VCFFileForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("New VCF file created successfully")
            return redirect('customadmin:dashboard')
    else:
        form = VCFFileForm()
    return render(request, 'customadmin/create_vcf.html', {'form': form})

def logout_view(request):
    """Handle admin logout"""
    logger.info(f"Admin user {request.user.username} logging out")
    logout(request)
    return redirect('customadmin:login')