from django.contrib import admin

from .models import Post,Comment,Profile,Notification,ThreadModel,MessageModel,Image,Tag

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
admin.site.register(Image)
admin.site.register(Tag)