from code.django_app.voice.models import Voice
# from django.shortcuts import render
from rest_framework import views, status
from rest_framework import Response
from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag

# Create your views here.


class VoiceListAPIView(views.APIView):
    # VOICE001を実装する
    def post(requests):
        return None


class VoiceCreateAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        # VOCIE002

        serializers = VoiceSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        saved_voice = serializers.instance
        # //あとでタグのリストをいれる
        tag_id_list = []
        for _id in tag_id_list:
            saved_voice.tag.add(Tag.objects.gete(id=_id))

        # タグの処理をする
        return Response(serializers.data, status.HTTP_201_CREATED)

    # テキストで送られてきたtagを分割して、新しいタグならデータベースに登録
    def save_tag(self, alltag, voice_id):
        # テキストで送られてきたtagを分割
        tags = alltag.split('#')

        for i in range(len(tags)):
            if Tag.objects.filter(name=tags[i]).exists():
                pass
            else:
                newtag = Tag(name=tags[i])
                newtag.save()


def get_tag_list(tag_txt):
    return []
