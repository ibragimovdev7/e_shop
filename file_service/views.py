from rest_framework import mixins, status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import File
from .serializers import FileSerializer, FileDetailSerializer


class FileView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FileSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        size = request.data.get('size')
        file = request.data.get('file')
        file_m = File.objects.create(
            name=name,
            size=size,
            file=file
        )
        return Response({
            'message': 'File uploaded!',
            'id': file_m.id,
            'file_url' : file_m.file.url
        })