"""
URL Configuration for cases app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Volunteer URLs
    path('volunteer/home/', views.volunteer_home, name='volunteer_home'),
    path('volunteer/report/', views.report_case, name='report_case'),
    
    # Shared URLs
    path('cases/', views.case_board, name='case_board'),
    
    # Team URLs
    path('team/dashboard/', views.team_dashboard, name='team_dashboard'),
    path('team/case/<int:case_id>/update/', views.update_case_status, name='update_case_status'),
    
    # Admin URLs (using /dashboard/ to avoid conflict with Django admin)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/appoint/<int:user_id>/', views.appoint_team_member, name='appoint_team_member'),
    path('dashboard/remove/<int:user_id>/', views.remove_team_member, name='remove_team_member'),
    
    # API URLs
    path('api/report/', views.api_report_case, name='api_report_case'),
]
