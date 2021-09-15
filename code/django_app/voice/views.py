from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag
from django.contrib.auth.models import User

import base64
# Create your views here.


class VoiceListAPIView(APIView):
    # VOICE001を実装する
    def post(requests):
        return None


class VoiceCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        input:
        {
            'user_uuid': text,
            'tags': text,
            'voice': text(base64 encoded)
        }
        '''
        # no user search
        user_uuid = request.data['user_uuid']
        tags = request.data['tags']
        voice = request.data['voice']

        voice_binary = base64.b64decode(voice)

        new_voice = Voice()
        new_voice.created_user = User.objects.get(username='root')
        new_voice.tags = Tag.objects.get(name=tags)
        new_voice.voice = voice_binary
        new_voice.save()

        # serializers = VoiceSerializer(data=request.data)
        # serializers.is_valid(raise_exception=True)
        # serializers.save()

        # saved_voice = serializers.instance
        # //あとでタグのリストをいれる
        # tag_id_list = []
        # for _id in tag_id_list:
        #     saved_voice.tag.add(Tag.objects.gete(id=_id))

        # タグの処理をする
        # return Response(serializers.data, status.HTTP_201_CREATED)
        return Response({'message': 'done'}, status.HTTP_201_CREATED)

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
