import os
import django
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from urllib.parse import urljoin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess.settings')
django.setup()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Получаем идентификатор чата из URL-параметров
            self.chat_type = None
            if 'personal_chat_id' in self.scope['url_route']['kwargs']:
                self.room_name = self.scope['url_route']['kwargs']['personal_chat_id']
                self.chat_type = 'personal'
            elif 'group_chat_id' in self.scope['url_route']['kwargs']:
                self.room_name = f'group_{self.scope["url_route"]["kwargs"]["group_chat_id"]}'
                self.chat_type = 'group'
            elif 'channel_id' in self.scope['url_route']['kwargs']:
                self.room_name = f'channel_{self.scope["url_route"]["kwargs"]["channel_id"]}'
                self.chat_type = 'channel'
            else:
                raise KeyError("personal_chat_id, group_chat_id, or channel_id is not found in URL")

            self.room_group_name = f'chat_{self.room_name}'

            # Присоединение к группе комнат
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Принятие WebSocket-соединения
            await self.accept()
            print(self)
        except KeyError as e:
            # В случае отсутствия personal_chat_id или group_chat_id в URL-параметрах
            print(f"4001 Error: {str(e)}")
            await self.close(code=4001)  # Закрываем соединение с кодом ошибки 4001
        except Exception as e:
            # В случае других ошибок
            print(f"An error occurred during WebSocket connection: {str(e)}")
            await self.close(code=4000)  # Закрываем соединение с кодом ошибки 4000

    async def disconnect(self, close_code):
        # Отсоединение от группы комнат
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обработка входящего сообщения от WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender')
        attachment_url = text_data_json.get('attachment_url')  # Путь к файлу
        attachment_type = text_data_json.get('attachment_type')
        
        # Отправка сообщения в группу комнат
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'attachment_url': attachment_url,
                'attachment_type': attachment_type,
            }
        )

    async def chat_message(self, event):
        # Получение данных сообщения из события
        message = event.get('message')
        sender = event.get('sender')
        attachment_url = event.get('attachment_url')
        attachment_type = event.get('attachment_type')
        timestamp = timezone.now().strftime('%d %B %Y г. %H:%M')

        # Формирование данных для отправки на клиент
        message_data = {
            'message': message,
            'sender': sender,
            'timestamp': timestamp,
            'attachment_url': attachment_url,
            'attachment_type': attachment_type,
        }
        # Отправка данных на клиент через WebSocket
        await self.send(text_data=json.dumps(message_data))
