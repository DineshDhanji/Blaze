from django.shortcuts import redirect
from django.urls import reverse

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)  # Allow access to admin users
        else:
            return redirect('BlazeAdministration:pageNotAccessible')  # Redirect non-admin users to another page
    return _wrapped_view


def anonymous_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)  # Allow access to non-logged-in or admin users
        else:
            return redirect('BlazeAdministration:index')  # Redirect logged-in non-admin users
    return _wrapped_view
