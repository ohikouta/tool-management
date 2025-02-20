import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # WebSocket からメッセージを受け取ったとき
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # グループにメッセージを送信
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # グループからメッセージを受け取ったとき
    async def chat_message(self, event):
        message = event['message']
        # WebSocket に送信
        await self.send(text_data=json.dumps({
            'message': message
        }))
