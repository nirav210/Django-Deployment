from django.shortcuts import render
from .forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'App/index.html')

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            profile = profile_form.save(commit=False)
            
            profile.user = user

            if 'profile_pic' in request.FILES:
                print('found it')
                
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {'user_form':user_form,
            'profile_form':profile_form,
            'registered':registered}
    
    return render(request,'App/registration.html', context)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE.')
        else:
            print('Someone tried to login and failed.')
            print(f'Username: {username} and Password: {password}')
            return HttpResponse('Invalid login details')

    else:
        return render(request, 'App/login.html')

@login_required
def special(request):
    return HttpResponse('You are logged in!!')

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))