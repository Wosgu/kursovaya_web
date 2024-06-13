from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с пользователем
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    notifications_enabled = models.BooleanField(default=True)
    sounds_enabled = models.BooleanField(default=True)
    dark_theme = models.CharField(max_length=10, default='light-theme')

    def is_online(self):
        last_seen = cache.get(f'last-seen-{self.user.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    def __str__(self):
        return f"Профиль {self.user.username}"

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

class Friendship(models.Model):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]
    
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"