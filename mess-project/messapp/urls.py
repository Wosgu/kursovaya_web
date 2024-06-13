#urls.py
from django.urls import path
from messapp.base.Views.home_views import home, search_users, save_theme
from messapp.base.Views.auth_views import register, user_login, user_logout
from messapp.base.Views.profile_views import profile, view_profile, subscribe, unsubscribe, send_friend_request_view, accept_friend_request_view, decline_friend_request_view, remove_friend_view, cancel_friend_request_view, edit_profile
from messapp.base.Views.chat_views import chat, pers, delete_personal_chat
from messapp.base.Views.group_view import create_group_chat, group_chat_detail, InvitationInChat_list, Invite
from messapp.base.Views.channel_view import create_channel, channel_detail, subscribeChannel, unsubscribeChannel
from messapp.base.Views.BetweenChats_view import Capturing_a_Message, Send_Capturing_a_Message, DeleteOneMessage
from messapp.base.Views.notifications_views import notification_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('save_theme/', save_theme, name='save_theme'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('pers/<int:receiver_id>/', pers, name='pers'),
    path('chat/<int:personal_chat_id>/', chat, name='chat'),
    path('search_users/', search_users, name='search_users'),
    path('view_profile/<int:user_id>/', view_profile, name='view_profile'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
    path('create_group_chat/', create_group_chat, name='create_group_chat'),
    path('group_chat_detail/<int:pk>/', group_chat_detail, name='group_chat_detail'),
    path('create_channel/', create_channel, name='create_channel'),
    path('channel_detail/<int:pk>/', channel_detail, name='channel_detail'),
    path('subscribeChannel/<int:channel_pk>/', subscribeChannel, name='subscribeChannel'),
    path('unsubscribeChannel/<int:channel_pk>/', unsubscribeChannel, name='unsubscribeChannel'),
    path('delete_personal_chat/<int:receiver_id>/', delete_personal_chat, name='delete_personal_chat'),
    path('Capturing_a_Message/<int:pk>/<str:TypeMessage>/', Capturing_a_Message, name='Capturing_a_Message'),
    path('Send_Capturing_a_Message/<str:TypeMessage>/<int:message>/<str:type_chat>/<int:pk>/', Send_Capturing_a_Message, name='Send_Capturing_a_Message'),
    path('DeleteOneMessage/<int:pk>/<str:TypeMessage>/', DeleteOneMessage, name='DeleteOneMessage'),
    path('send_friend_request/<int:user_id>/', send_friend_request_view, name='send_friend_request'),
    path('accept_friend_request/<int:user_id>/', accept_friend_request_view, name='accept_friend_request'),
    path('decline_friend_request/<int:user_id>/', decline_friend_request_view, name='decline_friend_request'),
    path('remove_friend/<int:user_id>/', remove_friend_view, name='remove_friend'),
    path('cancel_friend_request/<int:user_id>/', cancel_friend_request_view, name='cancel_friend_request'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('notification_view/', notification_view, name='notification_view'),
    path('InvitationInChat_list/<int:GroupChatId>', InvitationInChat_list, name='InvitationInChat_list'),
    path('Invite/<int:pk>/<int:GroupChatId>', Invite, name='Invite'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)