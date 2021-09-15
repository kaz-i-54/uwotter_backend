from .models import Tag
from .serializers import TagListSerializer
from voice.models import Voice

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class TagListAPIView(APIView):
    '''
    TAG001の実装
    '''
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagListSerializer(tags, many=True)
        return Response(serializer.data)
