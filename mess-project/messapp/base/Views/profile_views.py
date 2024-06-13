from django.shortcuts import render, redirect, get_object_or_404
from messapp.base.Forms.ProfileFroms import ProfileEditForm
from django.contrib.auth.decorators import login_required
from messapp.base.Models.UserModels import User, UserProfile, Subscription, Friendship
from messapp.base.Models.managers import *


@login_required
def profile(request):
    current_user = request.user

    if current_user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=current_user)
        user = request.user
        is_own_profile = request.user == user
        return render(request, 'profile.html', {'user': current_user, 'user_profile': user_profile, 'is_own_profile': is_own_profile})
    else:
        return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправляем пользователя на страницу профиля после успешного редактирования
    else:
        form = ProfileEditForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def view_profile(request, user_id=None):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    is_subscribed = False
    is_friends = is_friends_with(request.user, user)
    is_pending_sent = Friendship.objects.filter(from_user=request.user, to_user=user, status=Friendship.PENDING).exists()
    is_pending_received = Friendship.objects.filter(from_user=user, to_user=request.user, status=Friendship.PENDING).exists()
    pending_requests = get_pending_requests(request.user)
    
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, subscribed_to=user).exists()
    is_own_profile = request.user == user
    return render(request, 'profile.html', {
        'user': user,
        'user_profile': user_profile,
        'is_subscribed': is_subscribed,
        'is_own_profile': is_own_profile,
        'is_friends': is_friends,
        'is_pending_sent': is_pending_sent,
        'is_pending_received': is_pending_received,
        'pending_requests': pending_requests
    })

@login_required
def subscribe(request, user_id):
    if request.user.is_authenticated:
        subscribed_user = get_object_or_404(User, id=user_id)
        Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_user)
    return redirect('view_profile', user_id=user_id)

@login_required
def unsubscribe(request, user_id):
    if request.user.is_authenticated:
        subscribed_user = get_object_or_404(User, id=user_id)
        Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_user).delete()
    return redirect('view_profile', user_id=user_id)

@login_required
def send_friend_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not Friendship.objects.filter(from_user=request.user, to_user=user).exists():
        send_friend_request(request.user, user)
    return redirect('view_profile', user_id=user_id)

@login_required
def accept_friend_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    accept_friend_request(user, request.user)
    return redirect('view_profile', user_id=user_id)

@login_required
def decline_friend_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    decline_friend_request(user, request.user)
    return redirect('view_profile', user_id=user_id)

@login_required
def remove_friend_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    remove_friend(request.user, user)
    return redirect('view_profile', user_id=user_id)

@login_required
def friends_list_view(request):
    friends = get_friends(request.user)
    return render(request, 'friends_list.html', {'friends': friends})

@login_required
def cancel_friend_request_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    cancel_friend_request(request.user, user)
    return redirect('view_profile', user_id=user_id)