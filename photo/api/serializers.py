from rest_framework import serializers
from photo.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title','description','category','tags','webp_image','price','owner']
