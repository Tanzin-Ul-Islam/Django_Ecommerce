from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
#Auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate

from login_app.models import Profile
from login_app.forms import SignUpForm, ProfileForm

#messages
from django.contrib import messages

# Create your views here.
def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return HttpResponseRedirect(reverse('login_app:login'))
    return render(request, 'login_app/signup.html', context={'form':form})

def login_sys(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponse('Logged in')
    return render(request, 'login_app/login.html', context={'form':form})

@login_required
def logout_sys(request):
    logout(request)
    messages.warning(request, 'You are not logged in!!')
    return HttpResponse('Logged out')

@login_required
def user_profile(request):
    diction = {}
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated successfully!')
            form = ProfileForm(instance = profile)
    diction.update({'form':form})
    return render(request, 'login_app/change_profile.html', context=diction)

