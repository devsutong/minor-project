from django.db import models
from django.core import  exceptions 
from django.db.models import Sum, Count
from django.contrib.contenttypes.models import ContentType

class VoteManager(models.Manager):

    def upvote(self, obj, user): 

        ctype = ContentType.objects.get_for_model(obj) #post model
        try:
            v = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val(), activity_type='U') #vote item
            if v:
                v.delete()
        except exceptions.ObjectDoesNotExist:
            self.create(
                user=user, content_type=ctype, object_id=obj._get_pk_val(), activity_type='U'
            )


    def downvote(self, obj, user): 

        ctype = ContentType.objects.get_for_model(obj)
        try:
            v = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val(), activity_type='D') #vote item
            if v:
                v.delete()
        except exceptions.ObjectDoesNotExist:
            self.create(
                user=user, content_type=ctype, object_id=obj._get_pk_val(), activity_type='D'
            )
