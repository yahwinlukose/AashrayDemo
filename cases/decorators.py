"""
Custom decorators for role-based access control.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def volunteer_required(view_func):
    """Decorator to ensure user is authenticated (any role can access)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def team_required(view_func):
    """Decorator to ensure user is in Team group or is admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('login')
        
        if not (request.user.groups.filter(name='Team').exists() or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('volunteer_home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to ensure user is admin/superuser."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('login')
        
        if not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('volunteer_home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
