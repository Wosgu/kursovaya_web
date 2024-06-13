from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from messapp.base.Views.Helper.Helper import get_users_and_last_messages
from messapp.base.Models.UserModels import User, UserProfile
from messapp.base.Models.ChannelModels import Channel
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_POST

def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_chats, users_for_chat, last_messages_dict, last_group_messages_dict, read_messages_dict, read_group_messages_dict, subscribed_channels = get_users_and_last_messages(current_user)
        # Получаем значение dark_theme из профиля пользователя
        dark_theme = current_user.userprofile.dark_theme
        print(dark_theme)
        # Передаем в шаблон список пользователей, список групповых чатов и словарь с последними сообщениями
        # Создаем ответ
        response = render(request, 'home.html', {
            'username': current_user.username,
            'users': users_for_chat,
            'chats': user_chats,
            'last_messages': last_messages_dict,
            'last_group_messages': last_group_messages_dict, 
            'read_messages': read_messages_dict,
            'read_group_messages': read_group_messages_dict,
            'idUserCur': current_user.id,
            'channels': subscribed_channels,
        })

        # Сохраняем значение dark_theme в куках
        response.set_cookie('dark_theme', dark_theme)

        return response
    else:
        return redirect('login')

@require_POST
@login_required
def save_theme(request):
    theme = request.POST.get('theme')

    if theme in ['light-theme', 'dark-theme']:
        # Сохраняем предпочтение темы в профиле пользователя
        profile = request.user.userprofile
        profile.dark_theme = theme
        profile.save()

        # Возвращаем JSON-ответ об успешном сохранении предпочтений темы
        return JsonResponse({'message': 'Theme preference saved successfully'})
    else:
        # Возвращаем JSON-ответ об ошибке в случае неверных данных о теме
        return JsonResponse({'error': 'Invalid theme data received'}, status=400)
    
@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query)[:5]  # Limit to 10 results
        channels = Channel.objects.filter(name__icontains=query)[:5]  # Limit to 10 results
        user_results = []
        for user in users:
            user_profile = UserProfile.objects.get(user=user)
            user_results.append({
                'id': user.id,
                'type': 'user',
                'username': user.username,
                'avatar': user_profile.avatar.url,  # Replace with path to default avatar image
                'is_channel': False,
            })
        channel_results = []
        for channel in channels:
            channel_results.append({
                'id': channel.id,
                'type': 'channel',
                'name_c': channel.name,
                'avatar_c': channel.avatar.url if channel.avatar else '/path/to/default/channel_avatar.png'  # Replace with path to default channel avatar image
            })
        results = user_results + channel_results
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})