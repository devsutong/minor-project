from django.contrib import admin

from .models import Attachment, BlackList, Messages, ReportedMessages, UserTechInfo
# Register your models here.

admin.site.register(Messages)
admin.site.register(ReportedMessages)
admin.site.register(Attachment)
admin.site.register(UserTechInfo)
admin.site.register(BlackList)