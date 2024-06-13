from django.db import models
from django.contrib.auth.models import User

class GroupChatManager(models.Manager):
    def get_or_create_group_chat(self, name, members):
        group_chat = self.filter(name=name).filter(members__in=members).distinct().first()
        if not group_chat:
            group_chat = self.create(name=name)
            group_chat.members.add(*members)
        return group_chat
    
    def get_chat_messages(self):
        return MessageGroup.objects.filter(group_chat=self).order_by('timestamp')

class GroupChat(models.Model):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_chat.jpg')
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GroupChatManager()  # Привязка менеджера объектов

    def __str__(self):
        return self.name
    
class MessageGroup(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages_group', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    group_chat = models.ForeignKey(GroupChat, related_name='messages_group', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='private/messages/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Сообщение от {self.sender.username} в группе {self.group_chat.name}"