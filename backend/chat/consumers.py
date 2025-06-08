import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        message = content.get("message")
        user = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",  # 🟢 исправлено!
                "message": message,
                "user": user,
            }
        )

    async def chat_message(self, event):
        await self.send_json({
            "user": event["user"],
            "message": event["message"],
        })
