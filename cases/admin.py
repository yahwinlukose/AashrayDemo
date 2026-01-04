"""
Admin configuration for cases app.
"""
from django.contrib import admin
from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Admin interface for Case model."""
    
    list_display = ['case_type', 'place_spotted', 'priority', 'status', 'reported_by', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['case_type', 'place_spotted', 'needs']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_type', 'place_spotted', 'needs', 'priority', 'image')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'reported_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
