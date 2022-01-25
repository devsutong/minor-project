from django.conf import settings
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .exceptions import ClientError
from .models import Messages, UserTechInfo
from asgiref.sync import AsyncToSync
from .validators import blacklist_validator

from asgiref.sync import sync_to_async
import asyncio

User = get_user_model()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_profile(user):
    try:
        return UserTechInfo.objects.get_or_create(user=user)
    except UserTechInfo.DoesNotExist:
        return None

@database_sync_to_async
def save_profile(profile):
    try:
        profile.save()
    except:
        logger.error("Cannot save user technical profile in UserTechInfo")

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

@database_sync_to_async
def verify_user_id(user_id):
    try:
        return User.objects.get(id=user_id).id
    except User.DoesNotExist:
        return None

@database_sync_to_async
def get_user_id(user):
    try:
        return user.id
    except User.DoesNotExist:
        return None

class SocketConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat = None # of type authenticaion.User
    
    async def connect(self):
        await self.accept()
        await self.connect_user()
        
    async def receive_json(self, content, **kwargs):
        command = content.get("command", None)
        try:
            if command=="join_chat":
                if content.get('user_id'):
                    user_id = content.get('user_id')
                    task_get_user = asyncio.create_task(get_user(user_id))
                    task_get_user_id = asyncio.create_task(verify_user_id(user_id))
                    try:
                        self.chat = await task_get_user
                        local_user = await task_get_user_id
                        await self.send_json({"chat": local_user})
                    except User.DoesNotExist:
                        await self.send_json({"error": "USER_NOT_FOUND"})
                    except:
                        logger.debug("ERROR at consumer.SocketConsumer.recieve_json")
                        await self.send_json({"error": "BAD_REQUEST"})
            elif command == "leave_chat":
                self.chat = None
                await self.send_json({
                    "chat": self.chat
                })
            elif content.get('message'):
                await self.send_message(content.get('message'))
                logger.debug("consumers.receive_json: Sent")
        except ClientError as e:
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        await self.disconnect_user()
    
    async def connect_user(self):
        logger.debug("connecting user")
        user = self.scope["user"]
        task_get_profile = asyncio.create_task(get_profile(user))
        result  = await task_get_profile
        profile = result[0]
        task_save_profile = asyncio.create_task(save_profile(profile))
        profile.current_channel = self.channel_name
        profile.online = True
        await task_save_profile
        print(profile)
        await self.send_json({
            "user": user.username
        })

    async def chat_message(self, event):
        # task_get_user_id = asyncio.create_task(get_user_id(self.chat))
        # user_id = await task_get_user_id
        if event.get('source') == "signals":
            if event.get("sender") == "you" or (event.get('reciever') == "you" and self.chat == event.get('sender')):
                response = {
                    "message": event.get('message'),
                    "receiver": event.get('receiver'),
                    "sender": event.get('sender')
                }
            elif event.get('receiver') == "you":
                task_get_new_messages = asyncio.create_task(self.get_new_messages())
                new_messages = await task_get_new_messages
                # response = {
                #     "new_messages": [{
                #         "sender": message.get('sender'),
                #         "count": message.get('count')

                #     } for message in new_messages]
                # }
                # print(response)
                response = {
                    "message": event.get('message'),
                    "receiver": event.get('receiver'),
                    "sender": event.get('sender')
                }
            else:
                return False
            await self.send_json(response)

    @database_sync_to_async
    def send_message(self, message):
        if not self.chat:
            AsyncToSync(self.send_json)(
                {
                    "error": 'NO_CHAT_JOINED'
                }
            )
        else:
            try:
                blacklist_validator(message)
                Messages.objects.send_message(
                    sender=self.scope['user'],
                    # receiver=User.objects.get(id=self.chat),
                    receiver=self.chat,
                    message=message)
                logger.debug("from comsumer.send_message: Messages.objects.send_message")
                print("Sender: ", self.scope['user'])
                print("Reciever: ", self.chat)
                print("Message: ", message)

            except ValidationError:
                AsyncToSync(self.send_json)(
                    {
                        "error": 'BLACKLISTED_MESSAGE'
                    }
                )
    
    @database_sync_to_async
    def joined_chat(self):
        return self.chat

    @database_sync_to_async
    def disconnect_user(self):
        try:
            profile = UserTechInfo.objects.get(user=self.scope["user"])
            profile.current_channel = ""
            profile.online = False
            profile.save()
        except:
            pass

    @database_sync_to_async
    def get_new_messages(self):
        try :
            return Messages.objects.get_unread(self.scope["user"].id)
        except:
            print("Cannot get Messages")
