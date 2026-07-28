from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from datetime import datetime


class ChatConsumer(WebsocketConsumer):


    def save_message(self, username, message):

        from .models import Room, Message

        room = Room.objects.get(room_name=self.room_name)

        new_message = Message.objects.create(
            sender_name=username,
            message_detail=message,
            room=room
        )

        return new_message



    def edit_message(self, message_id, new_text):

        from .models import Message

        try:
            msg = Message.objects.get(id=message_id, sender_name=self.username, is_deleted=False)
            msg.message_detail = new_text
            msg.is_edited = True
            msg.save()
            return msg
        except Message.DoesNotExist:
            return None



    def delete_message(self, message_id):

        from .models import Message

        try:
            msg = Message.objects.get(id=message_id, sender_name=self.username)
            msg.is_deleted = True
            msg.message_detail = "This message was deleted"
            msg.save()
            return msg
        except Message.DoesNotExist:
            return None



    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.username = self.scope["session"]["username"]

        self.room_group_name = f"chat_{self.room_name}"


        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()



    def receive(self, text_data=None, bytes_data=None):

        print("MESSAGE RECEIVED:", text_data)

        data = json.loads(text_data)

        action = data.get("action", "send")


        # ---------- SEND NEW MESSAGE ----------
        if action == "send":

            message = data["message"]
            username = self.username

            new_message = self.save_message(username, message)

            message_data = {
                "id": new_message.id,
                "message": message,
                "username": username,
                "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_data
                }
            )


        # ---------- EDIT MESSAGE ----------
        elif action == "edit":

            message_id = data["id"]
            new_text = data["message"]

            updated_msg = self.edit_message(message_id, new_text)

            if updated_msg:

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "message_edited",
                        "id": updated_msg.id,
                        "message": updated_msg.message_detail
                    }
                )


        # ---------- DELETE MESSAGE ----------
        elif action == "delete":

            message_id = data["id"]

            deleted_msg = self.delete_message(message_id)

            if deleted_msg:

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "message_deleted",
                        "id": message_id
                    }
                )



    def chat_message(self, event):

        self.send(
            text_data=json.dumps({
                "type": "new_message",
                **event["message"]
            })
        )



    def message_edited(self, event):

        self.send(
            text_data=json.dumps({
                "type": "edit_message",
                "id": event["id"],
                "message": event["message"]
            })
        )



    def message_deleted(self, event):

        self.send(
            text_data=json.dumps({
                "type": "delete_message",
                "id": event["id"]
            })
        )