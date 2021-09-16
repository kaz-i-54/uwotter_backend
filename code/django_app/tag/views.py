from .models import Tag
from .serializers import TagListSerializer
from voice.models import Voice

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count


class TagListAPIView(APIView):
    '''
    TAG001の実装
    '''
    LIMIT_TAG_NUM = 20

    def get(self, request):
        tags = Tag.objects.annotate(Count("voice")) \
            .order_by("-voice__count")[:self.LIMIT_TAG_NUM]
        serializer = TagListSerializer(tags, many=True)
        response_json = {
            "result": list(serializer.data)
        }
        return Response(response_json, status=status.HTTP_200_OK)
        # return Response(serializer.data)
