from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from messapp.base.Views.Helper.Helper import get_users_and_last_messages
from messapp.base.Models.ChannelModels import Channel, SubscriberChannel, MessageChannel
from messapp.base.Forms.ChanelForms import ChannelForm, MessageChannelForm

@login_required
def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.super_admin = request.user
            channel.save()
            SubscriberChannel.objects.create(user=request.user, channel=channel)
            return redirect('channel_detail', pk=channel.pk)
    else:
        form = ChannelForm()
    return render(request, 'Dialog/create_channel.html', {'form': form})

@login_required
def channel_detail(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    current_user = request.user
    user_chats, users_for_chat, last_messages_dict, last_group_messages_dict, read_messages_dict, read_group_messages_dict, subscribed_channels = get_users_and_last_messages(current_user)
    if channel:
        channel = get_object_or_404(Channel, pk=pk)
        messages = channel.messages_channel.all()
        is_subscribed = False
        if SubscriberChannel.objects.filter(user=current_user, channel=channel).exists():
            is_subscribed = True
        for message in messages:
            message.view_count = message.view_count + 1
            message.save()
        if request.method == 'POST':
            if current_user != channel.super_admin:
                return redirect('channel_detail', pk=channel.pk)
            form = MessageChannelForm(request.user, channel, request.POST, request.FILES)

            if form.is_valid():
                content = form.cleaned_data['content']
                message = MessageChannel(sender=current_user, content=content, channel=channel)
                if 'attachment' in request.FILES:
                    message.attachment = request.FILES['attachment']
                message.save()
                return JsonResponse({
                    'message': message.content,
                    'attachment_url': str(message.attachment.url) if message.attachment else None,
                })
                return redirect('channel_detail', pk=channel.pk)
        else:
            form = MessageChannelForm(request.user, channel)
            if current_user != channel.super_admin:
                form = None
            

        return render(request, 'home.html', {
            'channel_pk': pk,
            'channelId': channel.id,
            'current_user': current_user,
            'users': users_for_chat,
            'messages': messages,
            'form': form,
            'chats': user_chats,
            'last_messages': last_messages_dict,
            'last_group_messages': last_group_messages_dict, 
            'read_messages': read_messages_dict,
            'read_group_messages': read_group_messages_dict,
            'idUserCur': current_user.id,
            'channels': subscribed_channels,
            'is_subscribed': is_subscribed,
            'typeChannel': True,
            'TypeMessage': 'Channel',
        })

    else:
        return redirect(request, 'home.html')

def subscribeChannel(request, channel_pk):
    if request.user.is_authenticated:
        channel = get_object_or_404(Channel, pk=channel_pk)
        user = request.user
        SubscriberChannel.objects.create(user=user, channel=channel)
    return redirect('channel_detail', pk=channel.pk)

def unsubscribeChannel(request, channel_pk):
    if request.user.is_authenticated:
        channel = get_object_or_404(Channel, pk=channel_pk)
        user = request.user
        SubscriberChannel.objects.get(user=user, channel=channel).delete()
    return redirect('channel_detail', pk=channel.pk)