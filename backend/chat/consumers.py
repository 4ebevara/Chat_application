import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = f"chat_{self.chat_id}"

        # проверяем, что пользователь аутентифицирован
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # присоединяемся к групповому каналу
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        # ожидаем, что content = {"message": "..."}
        message = content.get("message")
        user = self.scope["user"].username

        # рассылаем всем в группе
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": message,
                "user": user,
            }
        )

    async def chat_message(self, event):
        # отдаём сообщение клиентам
        await self.send_json({
            "user": event["user"],
            "message": event["message"],
        })
