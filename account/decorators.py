from django.http import HttpResponse
from django.shortcuts import redirect



def authenticated_user(view_func):
    def wrapper_fuc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
        
        
        
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                print('working ', allowed_roles)
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('myjob:home')
            
        return wrapper_func
    return decorator
