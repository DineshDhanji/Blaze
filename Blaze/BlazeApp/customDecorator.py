from django.shortcuts import redirect
from django.urls import reverse
from BlazeAdministration.views import page_not_found_404 

def normal_user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            return view_func(request, *args, **kwargs)  # Allow access to admin users
        else:
            # Redirect non-admin users to another page
            return page_not_found_404(request, exception=404)  

    return _wrapped_view