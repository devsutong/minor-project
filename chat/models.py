from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class MessagesManager(models.Manager):
    def inbox_for(self,user):
    
    #   Returns all messages that were received by the given user and are not
    #   marked as deleted.
        return self.filter(
            receiver =user,
            receiver_deleted_at__isnull=True,
       )

    def outbox_for(self, user):
    
    #   Returns all messages that were sent by the given user and are not
    #   marked as deleted.
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
    
    #   Returns all messages that were either received or sent by the given
    #   user and are marked as deleted.
        return self.filter(
            receiver=user,
            receiver_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
      )


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
        "Attachment", #because model | str
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