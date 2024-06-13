# managers.py
from django.contrib.auth.models import User
from django.db import models
from messapp.base.Models.UserModels import Friendship

def send_friend_request(from_user, to_user):
    friendship, created = Friendship.objects.get_or_create(from_user=from_user, to_user=to_user)
    return friendship

def accept_friend_request(from_user, to_user):
    friendship = Friendship.objects.filter(from_user=from_user, to_user=to_user, status=Friendship.PENDING).first()
    if friendship:
        friendship.status = Friendship.ACCEPTED
        friendship.save()
    return friendship

def decline_friend_request(from_user, to_user):
    friendship = Friendship.objects.filter(from_user=from_user, to_user=to_user, status=Friendship.PENDING).first()
    if friendship:
        friendship.status = Friendship.DECLINED
        friendship.save()
    return friendship

def remove_friend(user1, user2):
    # Удалить дружбу, если пользователь 1 и пользователь 2 взаимно добавили друг друга в друзья
    Friendship.objects.filter(
        (models.Q(from_user=user1, to_user=user2) | models.Q(from_user=user2, to_user=user1)) & 
        models.Q(status=Friendship.ACCEPTED)
    ).delete()

    # Удалить все запросы на дружбу между пользователями
    Friendship.objects.filter(
        (models.Q(from_user=user1, to_user=user2) | models.Q(from_user=user2, to_user=user1)) & 
        models.Q(status=Friendship.PENDING)
    ).delete()

def get_friends(user):
    friends = Friendship.objects.filter(
        (models.Q(from_user=user) | models.Q(to_user=user)) & 
        models.Q(status=Friendship.ACCEPTED)
    ).values_list('from_user', 'to_user')
    friend_ids = [friend[0] if friend[0] != user.id else friend[1] for friend in friends]
    return User.objects.filter(id__in=friend_ids)

def get_pending_requests(user):
    return Friendship.objects.filter(to_user=user, status=Friendship.PENDING)

def is_friends_with(user1, user2):
    return Friendship.objects.filter(
        (models.Q(from_user=user1, to_user=user2) | models.Q(from_user=user2, to_user=user1)) & 
        models.Q(status=Friendship.ACCEPTED)
    ).exists()

def cancel_friend_request(from_user, to_user):
    Friendship.objects.filter(from_user=from_user, to_user=to_user, status=Friendship.PENDING).delete()