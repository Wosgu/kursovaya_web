from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from messapp.base.Models.PersonalChatModels import Message
from messapp.base.Models.GroupChatModels import MessageGroup
from messapp.base.Models.ChannelModels import MessageChannel, SubscriberChannel
from messapp.base.Models.UserModels import User
from messapp.base.Models.PersonalChatModels import Message, User, PersonalChat
from messapp.base.Models.ChannelModels import Channel
from messapp.base.Models.GroupChatModels import GroupChat, MessageGroup

@login_required
def Capturing_a_Message(request, pk, TypeMessage):
    user_chats = GroupChat.objects.filter(members__in=[request.user])
    personal_chats = PersonalChat.objects.filter(members__in=[request.user])
    personal_chat_users = User.objects.none()
    for chat in personal_chats:
        other_user = chat.get_other_user(request.user)
        personal_chat_users = personal_chat_users | User.objects.filter(pk=other_user.pk)
    subscribed_channels = Channel.objects.filter(subscriberchannel__user=request.user, super_admin=request.user)    
    return render(request, 'Dialog/Between.html', 
                  {'user_chats': user_chats, 
                   'personal_chat_users_ids': personal_chat_users, 
                   'subscribed_channels': subscribed_channels, 
                   'message': pk,
                   'TypeMessage': TypeMessage,
                   })

@login_required
def Send_Capturing_a_Message(request, TypeMessage, message, type_chat, pk):
    if TypeMessage == 'Personal':
        old_message = get_object_or_404(Message, id=message)
        if old_message.sender != request.user and old_message.receiver != request.user:
            return HttpResponseForbidden("You do not have permission to forward this message.")
    elif TypeMessage == 'Group':
        old_message = get_object_or_404(MessageGroup, id=message)
        # Проверяем, что пользователь является членом группового чата
        if not old_message.group_chat.members.filter(pk=request.user.pk).exists():
            return HttpResponseForbidden("You do not have permission to forward this message.")
    else:
        old_message = get_object_or_404(MessageChannel, id=message)
        # Проверяем, что пользователь подписан на канал
        if not SubscriberChannel.objects.filter(user=request.user, channel=old_message.channel).exists():
            return HttpResponseForbidden("You do not have permission to forward this message.")

    if type_chat == 'personal':
        # Создаем или получаем существующий персональный чат между текущим пользователем и получателем
        receiver = User.objects.get(id=pk)
        in_chat = PersonalChat.objects.get_or_create_personal_chat(request.user, receiver)
        new_message = Message()
        new_message.sender = request.user
        new_message.content = 'Пересланное сообщение от ' + old_message.channel.name if TypeMessage == 'Channel: ' else 'Пересланное сообщение от ' + old_message.sender.username + ': ' + old_message.content
        new_message.personal_chat = in_chat
        new_message.receiver = in_chat.get_other_user(request.user)
        new_message.attachment = old_message.attachment
        new_message.save()
        return redirect('chat', personal_chat_id=in_chat.id)
    elif type_chat == 'group':
        # Получаем групповой чат, в который собираемся отправить сообщение
        group_chat = get_object_or_404(GroupChat, pk=pk)
        # Проверяем, что пользователь является членом группового чата
        if not group_chat.members.filter(pk=request.user.pk).exists():
            return HttpResponseForbidden("You do not have permission to forward this message.")
        new_message = MessageGroup()
        new_message.sender = request.user
        new_message.content = 'Пересланное сообщение от ' + old_message.channel.name if TypeMessage == 'Channel: ' else 'Пересланное сообщение от ' + old_message.sender.username + ': ' + old_message.content
        new_message.group_chat = group_chat
        new_message.attachment = old_message.attachment
        new_message.save()
        return redirect('group_chat_detail', pk=group_chat.id)
    else:
        # Получаем канал, в который собираемся отправить сообщение
        channel = get_object_or_404(Channel, pk=pk)
        # Проверяем, что пользователь является суперадмином канала
        if request.user != channel.super_admin:
            return HttpResponseForbidden("You do not have permission to forward this message.")
        new_message = MessageChannel()
        new_message.sender = request.user
        new_message.content = 'Пересланное сообщение от ' + old_message.channel.name if TypeMessage == 'Channel: ' else 'Пересланное сообщение от ' + old_message.sender.username + ': ' + old_message.content
        new_message.channel = channel
        new_message.attachment = old_message.attachment
        new_message.save()
        return redirect('channel_detail', pk=channel.id)

@login_required
def DeleteOneMessage(request, TypeMessage, pk):
    if TypeMessage == 'Personal':
        old_message = get_object_or_404(Message, id=pk)
        if old_message.sender != request.user and old_message.receiver != request.user:
            return HttpResponseForbidden("You do not have permission to forward this message.")
        old_message.delete()
        return redirect('chat', personal_chat_id=old_message.personal_chat.id)
    elif TypeMessage == 'Group':
        old_message = get_object_or_404(MessageGroup, id=pk)
        # Проверяем, что пользователь является членом группового чата
        if not old_message.group_chat.members.filter(pk=request.user.pk).exists():
            return HttpResponseForbidden("You do not have permission to forward this message.")
        old_message.delete()
        return redirect('group_chat_detail', pk=old_message.group_chat.id)
    else:
        old_message = get_object_or_404(MessageChannel, id=pk)
        # Проверяем, что пользователь подписан на канал
        if not SubscriberChannel.objects.filter(user=request.user, channel=old_message.channel).exists():
            return HttpResponseForbidden("You do not have permission to forward this message.")
        old_message.delete()
        return redirect('channel_detail', pk=old_message.channel.id)