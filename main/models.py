import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default='default_profile_image.png')
    location = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    number_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user_name} posted: {self.caption}'
