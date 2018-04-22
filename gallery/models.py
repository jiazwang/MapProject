from django.contrib.auth.models import Permission, User
from django.db import models


class Collection(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    collection_title = models.CharField(max_length=500)
    format = models.CharField(max_length=100)
    collection_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.collection_title + ' - ' + self.artist


class Picture(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    picture_title = models.CharField(max_length=250)
    picture_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.picture_title
