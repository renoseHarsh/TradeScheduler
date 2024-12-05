from django.shortcuts import redirect


def anonymous_required(view_func):
    """
    Decorator to ensure the user is not authenticated.
    Redirects authenticated users to the index page (dashboard:index).
    """

    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
