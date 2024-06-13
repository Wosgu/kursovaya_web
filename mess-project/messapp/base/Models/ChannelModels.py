from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_chat.jpg')
    name = models.CharField(max_length=255)
    super_admin = models.ForeignKey(User, related_name='super_admin_channels', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MessageChannel(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages_channel', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, related_name='messages_channel', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='private/messages/%Y/%m/%d/', null=True, blank=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Сообщение от {self.sender.username} в канале {self.channel.name}"

    def increment_view_count(self):
        self.view_count += 1
        self.save()

class MessageView(models.Model):
    message = models.ForeignKey(MessageChannel, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Статус просмотра для {self.subscriber.username} для сообщения {self.message.id}"
    
class SubscriberChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    # дополнительные поля для хранения информации о подписчиках на канал

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.channel.name}"