#routing.py
from django.urls import re_path 
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<personal_chat_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/group_chat/(?P<group_chat_id>\d+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/channel/(?P<channel_id>\d+)/$', ChatConsumer.as_asgi()),
]