from django.shortcuts import render, redirect
from .models import UserModel, BlogModel
from django.contrib.auth.models import User
from .forms import NewBlogForm
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        userRecord = UserModel.objects.get(user=user)
        if userRecord.role == 'Patient':
            blogs = BlogModel.objects.filter(isdraft=False)
            context = {
                'patient': True,
                'blogs': blogs
            }
        else:
            blogs = BlogModel.objects.filter(user=userRecord)
            context = {
                'doctor': True,
                'blogs': blogs
            }
        return render(request, 'core_app/home.html', context)
    else:
        return redirect('user_login')


def newblog(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        userRecord = UserModel.objects.get(user=user)
        if request.method == 'POST':
            blogform = NewBlogForm(request.POST, request.FILES)
            if blogform.is_valid():
                title = blogform.cleaned_data.get('title')
                image = blogform.cleaned_data.get('image')
                category = request.POST.get('category')
                summary = blogform.cleaned_data.get('summary')
                content = blogform.cleaned_data.get('content')
                isdraft = request.POST.get('isdraft') == 'True'
                
                blog = BlogModel.objects.create(user=userRecord, title=title, image=image, category=category, summary=summary, content=content, isdraft=isdraft, date=timezone.now())
                return redirect('home')
            else:
                blogform = NewBlogForm()
                context = {
                    'error': True,
                    'error_msg': 'Invalid Data',
                    'blogform': blogform,
                }
                return render(request, 'core_app/newblog.html', context)
        else:
            blogform = NewBlogForm()
            context = {
                'blogform': blogform,
            }
            return render(request, 'core_app/newblog.html', context)        
    else:
        return redirect('user_login')
        

def sortCategories(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        userRecord = UserModel.objects.get(user=user)
        if userRecord.role == 'Patient':
            if id == '1':
                blogs = BlogModel.objects.filter(isdraft=False, category='Mental Health')
            elif id == '2':
                blogs = BlogModel.objects.filter(isdraft=False, category='Heart Disease')
            elif id == '3':
                blogs = BlogModel.objects.filter(isdraft=False, category='Covid19')
            elif id == '4':
                blogs = BlogModel.objects.filter(isdraft=False, category='Immunization')    
            context = {
                'patient': True,
                'blogs': blogs
            }
            return render(request, 'core_app/home.html', context)
        else:
            if id == '1':
                blogs = BlogModel.objects.filter(user=userRecord, category='Mental Health')
            elif id == '2':
                blogs = BlogModel.objects.filter(user=userRecord, category='Heart Disease')
            elif id == '3':
                blogs = BlogModel.objects.filter(user=userRecord, category='Covid19')
            elif id == '4':
                blogs = BlogModel.objects.filter(user=userRecord, category='Immunization')    
            context = {
                'doctor': True,
                'blogs': blogs
            }
            return render(request, 'core_app/home.html', context)
    else:
        return redirect('user_login')


def blog(request, id):
    if request.user.is_authenticated:
        blog = BlogModel.objects.get(id=int(id))
        context = {
            'blog': blog
        }
        return render(request, 'core_app/blog.html', context)
    else:
        return redirect('user_login')