from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from messapp.base.Forms.ProfileFroms import ProfileEditForm
from messapp.base.Models.UserModels import User, UserProfile, Subscription, Friendship
from messapp.base.Models.managers import (
    send_friend_request,
    accept_friend_request,
    decline_friend_request,
    remove_friend,
    get_friends,
    get_pending_requests,
    is_friends_with,
    cancel_friend_request
)

@login_required
def notification_view(request):
        if request.user.is_authenticated:
            is_subscribed = False
            pending_requests = get_pending_requests(request.user)
            return render(request, 'Dialog/notification.html', {
                'is_subscribed': is_subscribed,
                'pending_requests': pending_requests
            })

