from django.contrib.auth.decorators import login_required
from messapp.base.Models.PersonalChatModels import Message, User
from messapp.base.Models.ChannelModels import Channel
from messapp.base.Models.GroupChatModels import GroupChat, MessageGroup
from django.db.models import Q
from messapp.base.Models.managers import get_friends

def get_users_and_last_messages(current_user):
    # Получаем список групповых чатов, в которых участвует текущий пользователь
    user_chats = GroupChat.objects.filter(members__in=[current_user])

   # Получаем пользователей, с которыми у нас есть персональный чат
    personal_chat_users_ids = current_user.personal_chats.values_list('members', flat=True).distinct().exclude(pk=current_user.pk)

    # Получаем пользователей, которые у нас в друзьях
    friends_ids = get_friends(current_user).values_list('id', flat=True)

    # Объединяем два QuerySet с помощью метода union
    users_for_chat_ids = User.objects.filter(Q(pk__in=personal_chat_users_ids) | Q(pk__in=friends_ids)).values_list('pk', flat=True)

    # Преобразуем QuerySet в список
    users_for_chat_ids = list(users_for_chat_ids)

    # Получаем список пользователей по их id, исключая текущего пользователя
    users_for_chat = User.objects.filter(pk__in=users_for_chat_ids).exclude(pk=current_user.pk)

    # Получаем последние сообщения для каждого пользователя
    last_messages_dict = {}
    for user in users_for_chat:
        last_message = Message.objects.filter(
            (Q(sender=current_user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=current_user))
        ).order_by('-timestamp').first()
        last_messages_dict[user.pk] = {'content': last_message.content, 'sender_id': last_message.sender_id} if last_message else None

    # Получаем последние сообщения для каждого группового чата
    last_group_messages_dict = {}
    for chat in user_chats:
        last_message = MessageGroup.objects.filter(group_chat=chat).order_by('-timestamp').first()
        last_group_messages_dict[chat.pk] = last_message.content if last_message else None

    # Получаем информацию о том, прочитано ли последнее сообщение для каждого пользователя
    read_messages_dict = {}
    for user in users_for_chat:
        last_message = Message.objects.filter(
            (Q(sender=current_user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=current_user))
        ).order_by('-timestamp').first()
        read_messages_dict[user.pk] = last_message.viewed if last_message else None

    # Получаем информацию о том, прочитано ли последнее сообщение для каждого группового чата
    read_group_messages_dict = {}
    for chat in user_chats:
        last_message = MessageGroup.objects.filter(group_chat=chat).order_by('-timestamp').first()
        read_group_messages_dict[chat.pk] = last_message.viewed if last_message else None
    
    # Получаем список каналов, на которые подписан текущий пользователь
    subscribed_channels = Channel.objects.filter(subscriberchannel__user=current_user)
    return user_chats, users_for_chat, last_messages_dict, last_group_messages_dict, read_messages_dict, read_group_messages_dict, subscribed_channels