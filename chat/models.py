from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.db.models import Q, Case, When, F, Count, Max

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class MessagesManager(models.Manager):

    def send_message(self, sender, reciever, message):
        try:
            sender = User.objects.get(id=sender)
            reciever = User.objects.get(id=reciever)
        except User.DoesNotExist:
            raise ValueError("User Does not Exist", 400)
        except Exception:
            ValueError("Request error", 400)
        else:
            if sender == reciever:
                raise ValueError("Cannot send message to self", 400)
        message = self.create(sender, reciever, message)
        return message

    def get_inbox(self, user):
        message = self.get_queryset().filter(reciever=user).order_by('-pk')
        return message

    def get_outbox(self, user):
        message = self.get_queryset().filter(sender=user)
        return message

    def read_message(self, mes_id):
        message = self.get_queryset().get(id=mes_id)
        if not message.read:
            message.read_datetime = timezone.now()
        message.save()
        return message

    def get_chats(self, user):
        qs =  self.get_queryset().filter(Q(sender=user) | Q(reciever=user)).annotate(
            user = Case(
                When(reciever=user, then=F('sender')),
                When(sender=user, then=F('reciever')),
                output_field=CharField(),
            ),
        ).values('user').annotate(
            unread_messages=Count( 
                'pk',
                filter = Q(reciever=user, read=False),
            ),
            last_message_id = Max('pk')
        ).order_by('-last_message_id')

        return qs

    def get_chat(self, sender_id, reciever_id):
        self.set_read(sender_id, reciever_id)
        return self.get_queryset().filter(
            Q(sender_id=sender_id, reciever_id=reciever_id) |
            Q(sender_id=reciever_id, reciever_id=sender_id)
        ).order_by('-pk')

    def get_unread(self, reciever_id):
        return self.get_queryset().filter(reciever_id=reciever_id, read=False).values("sender")\
            .annotate(count=Count("pk")).order_by("-count")
    
    def set_read(self, reciever_id, sender_id):
        return self.get_queryset().filter(sender_id=sender_id, reciever_id=reciever_id, read=False)\
            .update(read_datetime=timezone.now(), read=True)



class Messages(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
        ]
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    sender = models.ForeignKey(
        User,
        related_name='user_sender',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name='user_receiver',
        on_delete=models.CASCADE
    )

    message = models.TextField(
        blank=True,
        null=True
    )

    datetime = models.DateTimeField(
        auto_now=True
    )

    read = models.BooleanField(
        default=False
    )

    read_datetime = models.DateTimeField(
        null=True,
        default=None,
        blank=True
    )

    attachments = models.ManyToManyField(
        "Attachment", #because: model | str
        blank=True
    )

    objects = MessagesManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.read_datetime:
            self.read = True
        else:
            self.read = False
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "%s %s (%s) to %s %s (%s): %s" % (self.sender.first_name, self.sender.last_name,
                                                 self.sender.email,
                                                 self.receiver.first_name, self.receiver.last_name,
                                                 self.receiver.email,
                                                 self.message[:20])



class Attachment(models.Model):
    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    file = models.FileField(
        verbose_name="File",
        upload_to="attachments/"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class UserTechInfo(models.Model):
    user = models.OneToOneField(
        User,
        related_name="info",
        on_delete=models.CASCADE
    )

    current_channel = models.CharField(
        blank=True,
        default="",
        max_length=500
    )

    online = models.BooleanField(
        default=False
    )


class BlackList(models.Model):
    class Meta:
        verbose_name = "Black list"
        verbose_name_plural = "Black lists"

    word = models.CharField(
        max_length=200
    )

    regex = models.BooleanField(
        verbose_name='Regular expression'
    )

    enabled = models.BooleanField(
        default=True
    )

    def __str__(self):
        return "regex: /%s/" % self.word if self.regex else self.word


class ReportedMessages(models.Model):
    message = models.ForeignKey(
        "Messages",
        on_delete=models.CASCADE
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    datetime = models.DateTimeField(
        auto_now_add=True
    )

    comment = models.CharField(
        max_length=2000,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.message.message