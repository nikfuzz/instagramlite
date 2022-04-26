from rest_framework import serializers
from webapp.models import Albums, Pictures, Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('userId', 'username', 'password', 'firstName', 'lastName', 'albumId')

class AlbumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = ('albumId', 'name', 'pictureId', 'hashtags', 'isPublished')

class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = ('pictureId', 'picture', 'albumId', 'caption', 'fontColor')