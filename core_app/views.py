from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Appointment, BlogModel, UserModel
from .forms import NewBlogForm
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
import pickle



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


def doctors(request):
    if request.user.is_authenticated:
        doctors = UserModel.objects.filter(role='Doctor')
        context = {
            'patient': True,
            'doctors': doctors
        }
        return render(request, 'core_app/doctor.html', context)
    else:
        return redirect('user_login')


def bookAppointment(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        patient = UserModel.objects.get(user=user)
        doctor = UserModel.objects.get(id=id)
        
        if request.method == 'POST':
            speciality = request.POST.get('speciality')
            date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            temp = datetime.datetime.strptime(start_time, '%H:%M')
            end_time = temp + datetime.timedelta(minutes=45)
            end_time = end_time.time().strftime('%H:%M')
            appointment = Appointment.objects.create(patient=patient, doctor=doctor, speciality=speciality, date=date, start_time=start_time, end_time=end_time)

            credentials = pickle.load(open('token.pkl', 'rb'))
            service = build('calendar', 'v3', credentials=credentials)
            
            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            stime = datetime.datetime.strptime(start_time, "%H:%M")
            etime = datetime.datetime.strptime(end_time, "%H:%M")
            
            start_time = datetime.datetime(datem.year, datem.month, datem.day, stime.hour, stime.minute, 0)
            end_time = datetime.datetime(datem.year, datem.month, datem.day, etime.hour, etime.minute, 0)

            event = {
                'summary': 'Patient Appointment',
                'location': 'Mumbai',
                'description': 'Patient Name: ' + patient.first_name + ' ' + patient.last_name,
                'start': {
                    'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
                'attendees': [
                    {'email': doctor.email_id},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event = service.events().insert(calendarId='jrahul1112@gmail.com', body=event).execute()
            context = {
                'patient': True,
                'appointment': appointment
            }
            return render(request, 'core_app/confirmation.html', context)
        return render(request, 'core_app/appointment.html')
    else:
        return redirect('user_login')
