from tokenize import group
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm
from myjob.models import JobCategory,Jobs, JobAdmin
# from travelblog.models import Blog
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .decorators import allowed_users
# from travelblog.models import Author
# Create your views here.




def register_user(request):
    form = RegistrationForm(request.POST or None)
    
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
    
        if form.is_valid():
            user = form.save()
            print('this is the new user :', user)
            group = Group.objects.get(name='jobadmin')
            print('this is the group :', group)
            user.groups.add(group) 
            
            jobadmin = JobAdmin(user=user)
            jobadmin.save()
            print(dir(JobAdmin))
        
            return redirect('login')
        else:
            messages.error(request, 'unsuccessful signup check your data ')
    

    context = {'form':form}
    return render(request, 'account/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        # Email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully loged in ')
            return redirect('account:userdashboard_')
        else:
            messages.error(request, 'user not found')    
    return render(request, 'account/login.html')




def logout_user(request):
    logout(request)
    # return redirect(reverse('login'))
    return redirect("login")


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['jobadmin', 'blogadmin'])
def user_dashbaord(request):
           
    try:
        admin_job = request.user.jobadmin.jobs_set.all()
    except:
        return render(request, 'account/register.html')
    
    # if request.user.author:
    #     author_posts = request.user.author.get_author_posts()
    # else:
    #     pass
    context = {'admin_job':admin_job}
   
               
    #            }
    return render(request, 'account/dashboard.html', context)

