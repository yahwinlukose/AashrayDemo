"""
Setup script to create Django groups for Aashray platform.
Run this after migrations to set up the required groups.
"""

from django.contrib.auth.models import Group

def create_groups():
    """Create Team and Volunteer groups."""
    groups = ['Team', 'Volunteer']
    
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✓ Created group: {group_name}")
        else:
            print(f"- Group already exists: {group_name}")
    
    print("\n✓ Groups setup complete!")

if __name__ == '__main__':
    create_groups()
