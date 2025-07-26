import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from .forms import VCFFileForm
from .models import VCFFile
from functools import wraps

logger = logging.getLogger(__name__)

# Session-based admin_required decorator (unchanged from your original)
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('customadmin:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_view(request):
    """
    Handle admin authentication with hardcoded credentials (no database)
    """
    # If already logged in, redirect to dashboard
    if request.session.get('is_admin'):
        return redirect('customadmin:dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        ADMIN_CREDENTIALS = {
            'admin': 'admin123',
        }
        if username in ADMIN_CREDENTIALS and password == ADMIN_CREDENTIALS[username]:
            request.session['is_admin'] = True
            request.session.save()  # Explicit save
            return redirect('customadmin:dashboard')
        else:
            error = "Invalid login credentials."
    return render(request, 'customadmin/admin_login.html', {'error': error})

def logout_view(request):
    """Handle admin logout (clears session)"""
    request.session.flush()
    return redirect('customadmin:login')
    
@admin_required
def dashboard_view(request):
    """Admin dashboard view"""
    # Import MemberAccount model
    from members.models import MemberAccount
    active_users = MemberAccount.objects.count()
    total_vcf_files = VCFFile.objects.count()
    return render(request, 'customadmin/dashboard.html', {
        'active_users': active_users,
        'total_vcf_files': total_vcf_files,
    })

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
    form = VCFFileForm()
    return render(request, 'customadmin/create_vcf.html', {'form': form})