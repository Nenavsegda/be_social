from django.contrib import admin

from main.models import FollowersCount, LikePost, Post, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
