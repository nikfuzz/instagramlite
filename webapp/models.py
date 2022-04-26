from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=12)
    password = models.TextField()
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=50)
    albumId = ArrayField(models.IntegerField(null=True), default=list, blank=True)

# note: if an album is marked isPublished=false then it will be
# saved as a draft
class Albums(models.Model):
    albumId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    hashtags = ArrayField(models.CharField(max_length=20), blank=True)
    isPublished = models.BooleanField(default=False)
    username = models.ForeignKey("webapp.Users", on_delete=models.CASCADE)

class Pictures(models.Model):
    pictureId = models.AutoField(primary_key=True)
    picture = models.ImageField(upload_to="pictures/", null=True, blank=True)
    albumId = models.ForeignKey("webapp.Albums", on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    fontColor = models.CharField(max_length=100)