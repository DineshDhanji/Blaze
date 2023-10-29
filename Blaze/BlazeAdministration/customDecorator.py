from django.shortcuts import redirect
from django.urls import reverse
from . import views 

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)  # Allow access to admin users
        else:
            # Redirect non-admin users to another page
            return views.page_not_found_404(request, exception=404)  

    return _wrapped_view


def anonymous_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(
                request, *args, **kwargs
            )  # Allow access to non-logged-in or admin users
        elif request.user.is_authenticated and request.user.is_superuser:
            return redirect(
                "BlazeAdministration:dashboard"
            )  # Redirect logged-in non-admin users
        else:
            # Redirect non-admin users to another page
            return views.page_not_found_404(request, exception=404) 

    return _wrapped_view
