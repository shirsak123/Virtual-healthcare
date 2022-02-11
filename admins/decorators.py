from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/admindashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

def is_user_admin(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/admindashboard/login')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function