from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Messages
from . utils import get_user_info_from_instance

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@receiver (post_save, sender=Messages)
def send_message_to_socket(sender, instance, created, **kwargs):
    # if created:
    if created and hasattr(instance, 'receiver'):
        channel_layer = get_channel_layer()
        message = instance.message
        # print("instance.reciever.info.current_channel: ", instance.receiver.info.current_channel)
        if getattr(instance.receiver, "info", None) and instance.receiver.info.current_channel:
            channel_name = instance.receiver.info.current_channel
            print(channel_name)
            async_to_sync(channel_layer.send)(channel_name, {
                "type": "chat.message",
                "source": "signals",
                "message":  message,
                "receiver": "you",
                "sender": instance.sender.id
            })
        if getattr(instance.sender, "info", None) and instance.sender.info.current_channel:
            channel_name = instance.sender.info.current_channel
            print(channel_name)
            async_to_sync(channel_layer.send)(channel_name, {
                "type": "chat.message",
                "source": "signals",
                "message": message,
                "receiver": instance.receiver.id, 
                "sender": "you"
            })
    else:
        logger.debug("Whoops!, signal recieved but something went wrong!")
