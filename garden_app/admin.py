from django.contrib import admin

from .models import UserProfile,Plant,Pesticide,Disease,Schedule_Protection,Plant_diary,About_content,ContactMessage,ForumMessage,ForumReplyMessage

admin.site.register(UserProfile)
admin.site.register(Plant)
admin.site.register(Pesticide)
admin.site.register(Disease)
admin.site.register(Schedule_Protection)
admin.site.register(Plant_diary)
admin.site.register(About_content)
admin.site.register(ContactMessage)
admin.site.register(ForumMessage)
admin.site.register(ForumReplyMessage)

