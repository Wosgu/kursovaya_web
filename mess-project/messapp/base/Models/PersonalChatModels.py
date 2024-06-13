from django.db import models
from django.contrib.auth.models import User

class PersonalChatManager(models.Manager):
    def get_or_create_personal_chat(self, user1, user2):
        personal_chat = self.filter(members=user1).filter(members=user2).distinct().first()
        if not personal_chat:
            personal_chat = self.create()
            personal_chat.members.add(user1, user2)
        return personal_chat

class PersonalChat(models.Model):
    members = models.ManyToManyField(User, related_name='personal_chats')
    
    objects = PersonalChatManager()  # Привязка менеджера объектов

    def get_other_user(self, user):
        return self.members.exclude(pk=user.pk).first()

    def get_chat_messages(self):
        return Message.objects.filter(sender__in=self.members.all(), receiver__in=self.members.all()).order_by('timestamp')

    def __str__(self):
        return f"Personal chat between {', '.join([member.username for member in self.members.all()])}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    personal_chat = models.ForeignKey(PersonalChat, related_name='messages', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='private/messages/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"Сообщение от {self.sender.username} к {self.receiver.username} в чате {self.personal_chat.id}"