from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from django.db.models import Q, Case, When, F, Count, Max
from django.contrib.auth import get_user_model

User = get_user_model()

class MessagesManager(models.Manager):
    def send_message(self, **kwargs):
        if (kwargs.get('sender_id') or kwargs.get('sender')) and (kwargs.get('receiver_id') or kwargs.get('receiver')):
            try:
                sender = kwargs.get('sender') or User.objects.get(id=kwargs['sender_id'])
                receiver = kwargs.get('receiver') or User.objects.get(id=kwargs['receiver_id'])
                message = kwargs.get('message')
            except User.DoesNotExist:
                raise ValueError("User does not exist", 400)
            except Exception:
                raise ValueError("Request error", 400)
            else:
                if sender == receiver:
                    raise ValueError("You can't send message to yourself", 400)

            message = self.create(sender=sender, receiver=receiver, message=message)
            print("Message.send_message: Sent Message")
            print(message)
            return message
        else:
            print("Message.send_message: Cannot Send Message")
            return False
    def get_inbox(self, user):
        message = self.get_queryset().filter(receiver=user).order_by('-pk')
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
        qs =  self.get_queryset().filter(Q(sender=user) | Q(receiver=user)).annotate(
            user = Case(
                When(receiver=user, then=F('sender')),
                When(sender=user, then=F('receiver')),
                output_field=CharField(),
            ),
        ).values('user').annotate(
            unread_messages=Count( 
                'pk',
                filter = Q(receiver=user, read=False),
            ),
            last_message_id = Max('pk')
        ).order_by('-last_message_id')

        return qs

    def get_chat(self, sender_id, receiver_id):
        self.set_read(sender_id, receiver_id)
        return self.get_queryset().filter(
            Q(sender_id=sender_id, receiver_id=receiver_id) |
            Q(sender_id=receiver_id, receiver_id=sender_id)
        ).order_by('-pk')

    def get_unread(self, receiver_id):
        return self.get_queryset().filter(receiver_id=receiver_id, read=False).values("sender")\
            .annotate(count=Count("pk")).order_by("-count")
    
    def set_read(self, receiver_id, sender_id):
        return self.get_queryset().filter(sender_id=sender_id, receiver_id=receiver_id, read=False)\
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

    class Meta:
        verbose_name_plural = 'User Tech Infos'

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

    class Meta:
        verbose_name_plural = 'Reported Messages'

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

