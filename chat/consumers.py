import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.template.defaultfilters import date

class ChatConsumer(AsyncWebsocketConsumer):

    online_users = set()  # 在线用户集合

    async def connect(self):
        self.room_group_name = 'chat_room'

        # 将 WebSocket 连接加入到组中
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # upd user list
        self.username = self.scope["user"].username
        ChatConsumer.online_users.add(self.username)
        
        # 通知其他用户更新在线用户名单
        await self.update_user_list()

    async def disconnect(self, close_code):
        # 从组中移除 WebSocket 连接
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # upd user list
        ChatConsumer.online_users.remove(self.username)
        
        # 通知其他用户更新在线用户名单
        await self.update_user_list()

    # 接收来自 WebSocket 的消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        time_short = date(timezone.localtime(timezone.now()), "H:i")
        time_local = date(timezone.localtime(timezone.now()), "Y M jS H:i:s O")
        time_UTC = date(timezone.now(), "Y M jS H:i:s O")

        # 向组广播消息
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time_short': time_short,
                'time_local': time_local,
                'time_UTC': time_UTC
            }
        )

    # 接收来自组的消息
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time_short = event['time_short']
        time_local = event['time_local']
        time_UTC = event['time_UTC']

        # 通过 WebSocket 发送消息
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time_short': time_short,
            'time_local': time_local,
            'time_UTC': time_UTC
        }))

    # user list functions
    async def update_user_list(self):
        user_list = list(ChatConsumer.online_users)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_user_list',
                'user_list': user_list
            }
        )

    async def send_user_list(self, event):
        user_list = event['user_list']
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': user_list
        }))