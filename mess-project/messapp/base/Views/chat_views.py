from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from messapp.base.Views.Helper.Helper import get_users_and_last_messages
from messapp.base.Forms.PersonalChatForms import MessageForm
from messapp.base.Models.PersonalChatModels import PersonalChat
from messapp.base.Models.UserModels import User
from django.http import JsonResponse

@login_required
def chat(request, personal_chat_id=None):
    current_user = request.user
    user_chats, users_for_chat, last_messages_dict, last_group_messages_dict, read_messages_dict, read_group_messages_dict, subscribed_channels = get_users_and_last_messages(current_user)
    
    if personal_chat_id:
        try:
            personal_chat = PersonalChat.objects.get(id=personal_chat_id)
            receiver = personal_chat.get_other_user(current_user)
            HeaderAvatar = receiver.userprofile
            HeaderFirLasName = receiver.first_name, receiver.last_name, receiver.id
            messages = personal_chat.get_chat_messages()
            
            for message in messages:
                if message.receiver == current_user and not message.viewed:
                    message.viewed = True
                    message.save()
                    
        except PersonalChat.DoesNotExist:
            messages = None
            personal_chat = None
            receiver = None
        
        if request.method == 'POST':
            if not personal_chat.members.filter(pk=current_user.pk).exists():
                return redirect('chat', personal_chat_id=personal_chat.id)
                
            form = MessageForm(current_user, receiver, request.POST, request.FILES)
            
            if form.is_valid():
                message = form.save(commit=False)
                message.personal_chat = personal_chat
                message.save()
                
                return JsonResponse({
                    'message': message.content,
                    'attachment_url': str(message.attachment.url) if message.attachment else None,
                })
                
        else:
            form = MessageForm(sender=current_user, receiver=receiver)
            
        return render(request, 'home.html', {
            'current_user': current_user,
            'users': users_for_chat,
            'messages': messages,
            'receiver_id': receiver.id,
            'receiver_username': receiver.username,
            'form': form,
            'personal_chat_id': personal_chat_id,
            'chats': user_chats,
            'last_messages': last_messages_dict,
            'last_group_messages': last_group_messages_dict, 
            'read_messages': read_messages_dict,
            'read_group_messages': read_group_messages_dict,
            'idUserCur': current_user.id,
            'channels': subscribed_channels,
            'HeaderAvatar': HeaderAvatar,
            'HeaderFirLasName': HeaderFirLasName,
            'personal_chat': True,
            'TypeMessage': 'Personal',
        })
        
    else:
        return render(request, 'home.html', {
            'current_user': current_user,
            'users': users_for_chat,
            'receiver_id': None,
            'chats': user_chats,
        })

@login_required
def pers(request, receiver_id=None):
    current_user = request.user
    if receiver_id:
        try:
            receiver = User.objects.get(id=receiver_id)
            personal_chat = PersonalChat.objects.get_or_create_personal_chat(current_user, receiver)
            return redirect('chat', personal_chat_id=personal_chat.id)
        except PersonalChat.DoesNotExist:
            personal_chat = None

@login_required    
def delete_personal_chat(request, receiver_id):
    current_user = request.user
    receiver = User.objects.get(id=receiver_id)
    if receiver_id:
        try:
            personal_chat = PersonalChat.objects.get_or_create_personal_chat(current_user, receiver)
            personal_chat.delete()
            return redirect('home')
        except PersonalChat.DoesNotExist:
            personal_chat = None

