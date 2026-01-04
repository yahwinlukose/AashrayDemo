"""
Views for the cases app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Case
from .forms import UserRegistrationForm, CaseReportForm, CaseUpdateForm
from .decorators import volunteer_required, team_required, admin_required


# ============================================
# Authentication Views
# ============================================

def login_view(request):
    """Handle user login with role-based redirect."""
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return _redirect_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def register_view(request):
    """Handle user registration and auto-assign to Volunteer group."""
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-assign to Volunteer group
            volunteer_group, created = Group.objects.get_or_create(name='Volunteer')
            user.groups.add(volunteer_group)
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Aashray.')
            return redirect('volunteer_home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


def _redirect_by_role(user):
    """Helper function to redirect users based on their role."""
    if user.is_superuser:
        return redirect('admin_dashboard')  # Now redirects to /dashboard/
    elif user.groups.filter(name='Team').exists():
        return redirect('team_dashboard')
    else:
        return redirect('volunteer_home')


# ============================================
# Volunteer Views
# ============================================

@volunteer_required
def volunteer_home(request):
    """Volunteer dashboard/home page."""
    recent_cases = Case.objects.filter(reported_by=request.user)[:5]
    total_cases = Case.objects.filter(reported_by=request.user).count()
    
    context = {
        'recent_cases': recent_cases,
        'total_cases': total_cases,
    }
    return render(request, 'cases/volunteer_home.html', context)


@volunteer_required
def report_case(request):
    """Handle case reporting by volunteers."""
    if request.method == 'POST':
        form = CaseReportForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.reported_by = request.user
            case.save()
            messages.success(request, 'Case reported successfully! Thank you for your contribution.')
            return redirect('volunteer_home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CaseReportForm()
    
    return render(request, 'cases/report_case.html', {'form': form})


# ============================================
# Shared Views (All Authenticated Users)
# ============================================

@volunteer_required
def case_board(request):
    """Display all cases (accessible to all authenticated users)."""
    cases = Case.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        cases = cases.filter(status=status_filter)
    
    # Filter by priority if provided
    priority_filter = request.GET.get('priority')
    if priority_filter:
        cases = cases.filter(priority=priority_filter)
    
    context = {
        'cases': cases,
        'status_choices': Case.STATUS_CHOICES,
        'priority_choices': Case.PRIORITY_CHOICES,
        'current_status': status_filter,
        'current_priority': priority_filter,
    }
    return render(request, 'cases/case_board.html', context)


# ============================================
# Team Views
# ============================================

@team_required
def team_dashboard(request):
    """Team member dashboard with case management."""
    pending_cases = Case.objects.filter(status='PENDING')
    in_progress_cases = Case.objects.filter(status__in=['VALIDATED', 'IN_PROGRESS'])
    resolved_cases = Case.objects.filter(status__in=['RESOLVED', 'FORWARDED'])
    
    context = {
        'pending_cases': pending_cases,
        'in_progress_cases': in_progress_cases,
        'resolved_cases': resolved_cases,
        'total_pending': pending_cases.count(),
        'total_in_progress': in_progress_cases.count(),
        'total_resolved': resolved_cases.count(),
    }
    return render(request, 'cases/team_dashboard.html', context)


@team_required
def update_case_status(request, case_id):
    """Update case status (Team/Admin only)."""
    case = get_object_or_404(Case, id=case_id)
    
    if request.method == 'POST':
        form = CaseUpdateForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, f'Case status updated to {case.get_status_display()}.')
            return redirect('team_dashboard')
    
    return redirect('team_dashboard')


# ============================================
# Admin Views
# ============================================

@admin_required
def admin_dashboard(request):
    """Admin dashboard with full system overview."""
    all_cases = Case.objects.all()
    all_users = User.objects.all()
    team_members = User.objects.filter(groups__name='Team')
    volunteers = User.objects.filter(groups__name='Volunteer')
    
    context = {
        'total_cases': all_cases.count(),
        'pending_cases': all_cases.filter(status='PENDING').count(),
        'resolved_cases': all_cases.filter(status='RESOLVED').count(),
        'total_users': all_users.count(),
        'team_members': team_members,
        'volunteers': volunteers,
        'recent_cases': all_cases[:10],
    }
    return render(request, 'cases/admin_dashboard.html', context)


@admin_required
def appoint_team_member(request, user_id):
    """Appoint a user to Team group (Admin only)."""
    user = get_object_or_404(User, id=user_id)
    team_group, created = Group.objects.get_or_create(name='Team')
    
    if not user.groups.filter(name='Team').exists():
        user.groups.add(team_group)
        messages.success(request, f'{user.username} has been appointed as a Team member.')
    else:
        messages.info(request, f'{user.username} is already a Team member.')
    
    return redirect('admin_dashboard')


@admin_required
def remove_team_member(request, user_id):
    """Remove a user from Team group (Admin only)."""
    user = get_object_or_404(User, id=user_id)
    team_group = Group.objects.get(name='Team')
    
    if user.groups.filter(name='Team').exists():
        user.groups.remove(team_group)
        messages.success(request, f'{user.username} has been removed from Team.')
    
    return redirect('admin_dashboard')


# ============================================
# API Views
# ============================================

@csrf_exempt
@require_http_methods(["POST"])
def api_report_case(request):
    """
    API endpoint to receive case reports.
    POST /api/report/
    Accepts multipart/form-data with case information and image.
    """
    try:
        # Get user (you may want to implement token-based auth here)
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        # Create case from POST data
        case = Case.objects.create(
            case_type=request.POST.get('case_type'),
            place_spotted=request.POST.get('place_spotted'),
            needs=request.POST.get('needs'),
            priority=request.POST.get('priority', 'MEDIUM'),
            image=request.FILES.get('image'),
            reported_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Case reported successfully',
            'case_id': case.id
        }, status=201)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
