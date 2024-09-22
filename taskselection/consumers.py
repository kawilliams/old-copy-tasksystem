# taskselection/consumers.py
# from channels import Group
# from channels.sessions import channel_session
# #from .models import Room

# @channel_session
# def ws_connect(message):
#   print(message.content)
#   # TODO: check for authentication
#   Group('task_selections').add(message.reply_channel)
#   message.channel_session['tasks'] = 'task_selections'
#   message.reply_channel.send({'accept': True})

# @channel_session
# def ws_disconnect(message):
#   #print('disconnect ' + message.content)
#   Group('task_selections').discard(message.reply_channel)

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TaskSelectionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Print connection info (similar to your print(message.content))
#         print(f"WebSocket connected: {self.scope}")
        
#         # TODO: check for authentication (you can implement this here)

#         # Join the group
#         await self.channel_layer.group_add("task_selections", self.channel_name)
        
#         # Store group name in session (similar to message.channel_session['tasks'])
#         self.scope['session']['tasks'] = 'task_selections'
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the group
#         await self.channel_layer.group_discard("task_selections", self.channel_name)
#         print(f"WebSocket disconnected: {close_code}")

#     # You can add methods to handle receiving messages if needed
#     async def receive(self, text_data):
#         print(f"Received message: {text_data}")
#         # Echo the received message back to the client
#         await self.send(text_data=f"Echo: {text_data}")

#     # Method to send messages to the group (new functionality)
#     async def task_message(self, event):
#         message = event['message']
#         await self.send(text_data=message)

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskSelectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #await self.channel_layer.group_add("task_selections", self.channel_name)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        #await self.channel_layer.group_discard("task_selections", self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    # async def task_message(self, event):
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))