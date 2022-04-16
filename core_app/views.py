from django.shortcuts import render, redirect
from .models import UserModel, Address
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        userRecord = UserModel.objects.get(user=user)
        context = {
            'userRecord': userRecord
        }
        return render(request, 'core_app/home.html', context)
    else:
        return redirect('user_login')