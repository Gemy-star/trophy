
"""
Custom context processors
"""
from main.models import Announcement

def portal_data(request):
    """Define common context variables to be used in views/templates"""
    announcements = Announcement.objects.all().order_by('-date')[:3]
    ctx = {"announcements": announcements}
    return ctx
