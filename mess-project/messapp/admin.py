#admin.py
from django.contrib import admin
from messapp.base.Models.UserModels import UserProfile, Friendship
from messapp.base.Models.PersonalChatModels import Message, PersonalChat
from messapp.base.Models.GroupChatModels import GroupChat, MessageGroup
from messapp.base.Models.ChannelModels import Channel, MessageChannel, MessageView

# Регистрируем модели в админке
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(PersonalChat)
admin.site.register(GroupChat)
admin.site.register(MessageGroup)
admin.site.register(Channel)
admin.site.register(MessageChannel)
admin.site.register(MessageView)
admin.site.register(Friendship)
