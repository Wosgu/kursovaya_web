from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from messapp.base.Views.Helper.Helper import get_users_and_last_messages
from messapp.base.Models.GroupChatModels import GroupChat, MessageGroup
from messapp.base.Forms.GroupChatForms import GroupChatForm, MessageGroupForm
from messapp.base.Models.managers import get_friends
from messapp.base.Models.UserModels import User


@login_required
def create_group_chat(request):
    friends = get_friends(request.user) # Получаем список друзей
    if request.method == 'POST':
        form = GroupChatForm(request.user, friends, request.POST)
        if form.is_valid():
            group_chat = form.save()
            group_chat.members.add(request.user)
            message = MessageGroup(sender=request.user, content='Беседа создана!😁', group_chat=group_chat)
            message.viewed = True
            message.save()
            return redirect('group_chat_detail', pk=group_chat.pk)
    else:
        form = GroupChatForm(request.user, friends)
    return render(request, 'Dialog/create_group_chat.html', {'form': form})

@login_required
def group_chat_detail(request, pk):
    group_chat = get_object_or_404(GroupChat, pk=pk)
    current_user = request.user
    user_chats, users_for_chat, last_messages_dict, last_group_messages_dict, read_messages_dict, read_group_messages_dict, subscribed_channels = get_users_and_last_messages(current_user)
    if group_chat:
        group_chat = get_object_or_404(GroupChat, pk=pk)
        messages = group_chat.messages_group.all()
        for message in messages:
            if message.sender != current_user and not message.viewed:
                message.viewed = True
                message.save()
        if request.user not in group_chat.members.all():
            return redirect('home')  # перенаправляем на страницу со списком групповых чатов

        if request.method == 'POST':
            form = MessageGroupForm(request.user, group_chat, request.POST, request.FILES)

            if form.is_valid():
                content = form.cleaned_data['content']
                message = MessageGroup(sender=current_user, content=content, group_chat=group_chat)
                if 'attachment' in request.FILES:
                    message.attachment = request.FILES['attachment']
                message.save()
                return JsonResponse({
                    'message': message.content,
                    'attachment_url': str(message.attachment.url) if message.attachment else None,
                })
                return redirect('group_chat_detail', pk=group_chat.pk)  # Используйте идентификатор персонального чата для перенаправления
        else:
            form = MessageGroupForm(request.user, group_chat)

        return render(request, 'home.html', {
            'group_chat': group_chat,
            'messages': messages,
            'form': form,
            'users': users_for_chat,
            'chats': user_chats,
            'last_messages': last_messages_dict,
            'last_group_messages': last_group_messages_dict,
            'read_messages': read_messages_dict,
            'read_group_messages': read_group_messages_dict,
            'idUserCur': current_user.id,
            'channels': subscribed_channels,
            'TypeMessage': 'Group',
            'HeaderAvatar': group_chat.avatar,
            'HeaderName': group_chat.name,
            'CounterChel': group_chat.members.count()
        })

    else:
        return redirect(request, 'home.html')
    
@login_required
def InvitationInChat_list(request, GroupChatId):
    if request.user.is_authenticated:
        # Получаем пользователей, которые у нас в друзьях
        friends = get_friends(request.user)

        # Получаем групповой чат
        group_chat = get_object_or_404(GroupChat, pk=GroupChatId)

        # Исключаем из друзей тех, кто уже является членом группового чата
        friends_not_in_chat = friends.exclude(pk__in=group_chat.members.values_list('pk', flat=True))

        return render(request, 'Dialog/InvitationInChat_list.html', {
        'friends': friends_not_in_chat,
        'GroupChatId': GroupChatId,
        })

@login_required
def Invite(request, pk, GroupChatId):
    if request.user.is_authenticated:
        # Получаем пользователя, которого нужно добавить в чат
        user_to_add = get_object_or_404(User, pk=pk)
        # Получаем групповой чат
        group_chat = get_object_or_404(GroupChat, pk=GroupChatId)
        # Добавляем пользователя в чат
        group_chat.members.add(user_to_add)
        # Перенаправляем на страницу чата
        return redirect('group_chat_detail', pk=GroupChatId)
    