from web.comics.models import Comic, File
from rest_framework import serializers

class ComicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ('name', 'description')

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        # fields = ('comic', 'num', 'filename', 'alt_text', 'annotation')
