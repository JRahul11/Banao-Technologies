from django.shortcuts import render, redirect
from core_app.models import UserModel, Address
from django.contrib.auth import login, logout, authenticate
from .forms import NewUserForm, NewAddressForm
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        except Exception as e:
            print(e)
            context = {
                'error': True,
                'error_msg': 'Check Credentials'
            }
            return render(request, 'auth_app/user_login.html', context)
    else:
        return render(request, 'auth_app/user_login.html')

def user_signup(request):
    if request.method == 'POST':
        userform = NewUserForm(request.POST, request.FILES)
        addressform = NewAddressForm(request.POST)
        if userform.is_valid() and addressform.is_valid():
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')
            username = userform.cleaned_data.get('username')
            email_id = userform.cleaned_data.get('email_id')
            password1 = userform.cleaned_data.get('password')
            password2 = request.POST.get('password2')
            address_line1 = addressform.cleaned_data.get('address_line1')
            city = addressform.cleaned_data.get('city')
            state = addressform.cleaned_data.get('state')
            pincode = addressform.cleaned_data.get('pincode')
            role = request.POST.get('role')
            profile_picture = userform.cleaned_data.get('profile_picture')
            try:
                user = User.objects.get(username=username)
                userform = NewUserForm()
                addressform = NewAddressForm()
                context = {
                    'userform': userform,
                    'addressform': addressform,
                    'error': True,
                    'error_msg': 'Username Exists'
                }
                return render(request, 'auth_app/user_signup.html', context)
            except:
                if(password1 == password2):
                    address = Address.objects.create(address_line1=address_line1, city=city, state=state, pincode=pincode)
                    user = User.objects.create_user(username=username, password=password1)
                    customUser = UserModel.objects.create(user=user, first_name=first_name, last_name=last_name, profile_picture=profile_picture, email_id=email_id, address=address, role=role)
                    return redirect('user_login')
                else:
                    userform = NewUserForm()
                    addressform = NewAddressForm()
                    context = {
                        'userform': userform,
                        'addressform': addressform,
                        'error': True,
                        'error_msg': 'Password does not match'
                    }
                    return render(request, 'auth_app/user_signup.html', context)
        else:
            userform = NewUserForm()
            addressform = NewAddressForm()
            context = {
                'userform': userform,
                'addressform': addressform,
                'error': True,
                'error_msg': 'Invalid Data'
            }
            return render(request, 'auth_app/user_signup.html', context)
        
    else:
        userform = NewUserForm()
        addressform = NewAddressForm()
        context = {
            'userform': userform,
            'addressform': addressform,
        }
        return render(request, 'auth_app/user_signup.html', context)
    

def user_logout(request):
    logout(request)
    return redirect('user_login')