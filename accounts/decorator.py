from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/accounts/dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

def is_user_patient(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_patient:
            return redirect('/accounts/dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function