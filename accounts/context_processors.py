from django.contrib.auth.models import User

def auth_context(request):
    """Add authentication context to all templates."""
    # Count users to determine if this is a new installation
    user_count = User.objects.count()
    return {
        'is_new_installation': user_count <= 1,  # Only the admin account exists
    }
