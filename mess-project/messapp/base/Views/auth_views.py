from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from messapp.base.Models.UserModels import UserProfile
from messapp.base.Forms.AuthorizationForms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user_profile = UserProfile(user=user)
                user_profile.notifications_enabled = True
                user_profile.sounds_enabled = True
                user_profile.avatar = 'avatars/default_avatar.png'
                user_profile.background_image = 'background/default_back.png'
                user_profile.save()
                login(request, user)
                return redirect('home')
            except Exception as e:
                return render(request, 'Authorization/register.html', {'form': form})
        else:
            form = RegistrationForm()
            return render(request, 'Authorization/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'Authorization/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
        return render(request, 'Authorization/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'Authorization/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')