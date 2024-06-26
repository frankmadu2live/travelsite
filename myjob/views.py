from genericpath import exists
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobAdmin, Jobs, JobCategory, City
from .forms import JobListForm
from django.db.models.query import QuerySet
from django.db.models import Q
from django.urls.base import reverse
from django.core.checks import messages
from django.db.models import Q

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required, permission_required

# the job admin
from django.core.exceptions import ObjectDoesNotExist


def searchjob(request):
    queryset = Jobs.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(job_title__icontains=query) |
            Q(job_description__icontains=query)
        ).distinct()
    context={
        'queryset':queryset
    }
    return render(request, 'myjob/search_result.html', context)
    
    

def createJobAdmin(user):
    jobadmin = JobAdmin.objects.create(user=user)
    jobadmin.save()
    return jobadmin


# def getJobAdmin(user):
#     jobadmin = JobAdmin.objects.filter(user=user)
    
#     if jobadmin.exists :
        
#         print('this is the jober : ', jobadmin[0])
#         return jobadmin[0] 
#     else:
#         passfrom django.core.exceptions import ObjectDoesNotExist

def get_job_admin(user: User) -> JobAdmin:
    try:
        return JobAdmin.objects.get(user=user)
    except ObjectDoesNotExist:
        createJobAdmin(user)
        return get_job_admin(user)
        # raise ValueError(f"No JobAdmin found for user {user.username}")
    

def jobhome(request):
    
    most_recent_post = Jobs.objects.order_by("-post_date")[0:6]

    
    featured_post = Jobs.objects.all()
    # added this to avoid inconsistendcy with the pagenation
    featured_post = featured_post.order_by('id')
    
    paginator = Paginator(featured_post, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages) 
        
    # category view
    category_list = JobCategory.objects.all()
    city_list = City.objects.all()
    context = {
        # "category_count":category_count,
        
        'city_list' : city_list,
        'category_list' : category_list,
        'queryset':paginated_queryset,
        "page_request_var":page_request_var ,
        "featured_post":featured_post,
        "most_recent_post":most_recent_post, 
    }

    # return render(request, 'accounts/register.html', context)
    return render(request, 'myjob/jobhome.html', context)



def city_job(request, id):
    title = 'city'
    
    cityobj = get_object_or_404(City, id=id)
    cityjobs = cityobj.jobs_set.all()
    
    paginator = Paginator(cityjobs, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages) 
        
    context = {
        'cityobj':cityobj,
        'queryset':paginated_queryset,
        'title':title,
        }
    return render(request, 'myjob/cityjobs.html', context)
    

def catjobs(request, id):
    title = 'category'
    catobj = get_object_or_404(JobCategory, id=id)
    catjobs = catobj.jobs_set.all()
    
    paginator = Paginator(catjobs, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages) 
        
    context = {
        'catobj':catobj,
        'queryset':paginated_queryset,
        'title':title,
        }
    return render(request, 'myjob/job_category.html', context)


def jobDetail(request, id):
    most_recent = Jobs.objects.order_by('-post_date')[:3]
    post = get_object_or_404(Jobs, id=id)
    
    context = {
        'post':post,
        'most_recent':most_recent,
        # 'commentform':commentform,
    
    }
   
    return render(request, 'myjob/jobdetail.html', context)

def createJob(request):
    title = "CREATE"
    err_msg = ''
    message = ""
    form = JobListForm()
    
    if request.user.is_authenticated:
        try:
            form = JobListForm(request.POST or None, request.FILES or None)
            user = request.user          
            jobadmin = get_job_admin(user)
            print('this is the : {}' .format(jobadmin))
            if request.method == "POST":
                if form.is_valid():
                    form.instance.job_admin = jobadmin
                    form.save()
                    return redirect(reverse("job-detail", kwargs={
                        'id':form.instance.id
                    }))
                else:
                    print('this complete the form fields')
        except IntegrityError as e :
            e = "please contact admin  to gain access to post your blog"
            err_msg = e
            print(err_msg)
            return redirect('myjob')
    else:
        return redirect('accounts:login')
    message = err_msg
    context = {
        'jobadmin':jobadmin,
        "title":title,
        'message':message,
        'form':form,
        }

    return render(request, 'myjob/create_job.html', context)

   # job post update

def updateJob(request, id):
    title = "UPDATE"
    err_msg=''
    message = ""
    post = get_object_or_404(Jobs, id=id)
    form = JobListForm(request.POST or None, request.FILES or None, instance=post)
    user = request.user
    jobadmin = get_job_admin(user)
    
    if request.method == "POST":
        if form.is_valid():
            form.instance.job_admin = jobadmin
            form.save()

            return redirect(reverse("job-detail", kwargs={
                'id':form.instance.id
            }))

    
    message = err_msg
    
    context = {
        "title":title,
        
        'message':message,
        'form':form,
        }

    
    return render(request, 'myjob/create_job.html', context)


def delete_job(request, id):
    jobpost = get_object_or_404(Jobs, id=id)
    print(dir(jobpost))
    jobpost.delete()
    return redirect('account:dashboard')