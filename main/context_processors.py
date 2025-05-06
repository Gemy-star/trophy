
"""
Custom context processors
"""

def portal_data(request):
    """Define common context variables to be used in views/templates"""
    ctx = {"announcements": "None"}
    return ctx
