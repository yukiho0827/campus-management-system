from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import datetime


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 握手
        self.accept()
        # print('已连接')
        # 获取群号
        group = self.scope['url_route']['kwargs'].get("group")
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)
        # 给客户端发送消息

    def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get("group")
        # print(message)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text, user = message['text'].split('|')
        # content = time + "|" + message['text'],
        content = rf"{user}|{time}|{text}"
        async_to_sync(self.channel_layer.group_send)(group, {'type': "xx.oo", 'message': content})

    def xx_oo(self, event):
        text = event['message']
        # 给组里的每一个人发送消息
        self.send(text)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("group")
        # print('断开连接')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()

