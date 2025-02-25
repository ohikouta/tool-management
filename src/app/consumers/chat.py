import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import ChatMessage, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # グループに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f'WebSocket connected. room_name: {self.room_name}')

    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f'WebSocket disconnected.')

    # WebSocket からメッセージを受け取ったとき
    async def receive(self, text_data):
        print("あーーーー")
        data = json.loads(text_data)
        message = data['message']
        # ここでは、クライアントから sender を送信しない前提で、
        # 認証済みユーザーを sender として利用する方法
        user = self.scope.get("user")
        sender_username = user.username if user and user.is_authenticated else "Anonymous"

        await self.save_message(self.room_name, sender_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
            }
        )

    # グループからメッセージを受け取ったとき
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        # WebSocket に送信
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,

        }))

    @database_sync_to_async
    def save_message(self, room_name, sender_username, message):
        print(f"Saving message: room={room_name}, sender={sender_username}, message={message}")
        # チャットルームの取得（存在しない場合は作成する等の処理も可能）
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        sender, _ = User.objects.get_or_create(username=sender_username)
        ChatMessage.objects.create(room=room, sender=sender, message=message)