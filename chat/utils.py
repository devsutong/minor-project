from rest_framework import serializers
from collections import OrderedDict
from .models import Attachment

import logging

logger = logging.getLogger(__name__)


def get_user_info_from_instance(instance):
    info = {
        "id": instance.id,
        "name": "{} {}".format(instance.first_name, instance.last_name),
        "email": instance.email
    }
    return info