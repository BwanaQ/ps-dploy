from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def superuser_required(view_func):
    """
    Decorator for views that checks if the user is a superuser,
    redirects to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/admin/login/',
    )
    return actual_decorator(view_func)