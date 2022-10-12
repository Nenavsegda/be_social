from django.contrib import admin
from main.models import LikePost, Post, Profile


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
