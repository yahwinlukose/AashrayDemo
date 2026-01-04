"""
Models for the cases app.
"""
from django.db import models
from django.contrib.auth.models import User


class Case(models.Model):
    """
    Model representing a hunger/vulnerability case reported by volunteers.
    """
    
    # Priority choices
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VALIDATED', 'Validated'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('FORWARDED', 'Forwarded'),
    ]
    
    case_type = models.CharField(max_length=100, help_text="Type of case (e.g., Food Shortage, Malnutrition)")
    place_spotted = models.CharField(max_length=255, help_text="Location where the case was spotted")
    needs = models.TextField(help_text="Description of needs and situation")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    image = models.ImageField(upload_to='case_images/', blank=True, null=True, help_text="Optional image of the situation")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'
    
    def __str__(self):
        return f"{self.case_type} - {self.place_spotted} ({self.status})"
    
    def get_priority_badge_class(self):
        """Return Bootstrap badge class based on priority."""
        return {
            'HIGH': 'danger',
            'MEDIUM': 'warning',
            'LOW': 'info',
        }.get(self.priority, 'secondary')
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class based on status."""
        return {
            'PENDING': 'secondary',
            'VALIDATED': 'primary',
            'IN_PROGRESS': 'warning',
            'RESOLVED': 'success',
            'FORWARDED': 'info',
        }.get(self.status, 'secondary')
