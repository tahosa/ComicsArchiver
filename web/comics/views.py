from web.comics.models import Comic, File
from rest_framework import viewsets
from web.comics.serializers import ComicSerializer, FileSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class ComicViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def comics_list(request):
    if request.method == 'GET':
        comics = Comic.objects.all()
        serializer = ComicSerializer(comics, many=True)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse(status_code=404)
