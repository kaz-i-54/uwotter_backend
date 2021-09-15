# from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag

# from datetime import datetime
import base64
# Create your views here.


class VoiceListAPIView(APIView):
    # VOICE001を実装する
    def get(self, request, *args, **kwargs):
        if "now" not in request.data.keys():
            return Response(None, status.status.HTTP_400_BAD_REQUEST)

        current_time = request.data["now"]

        if "tag_uuid" in request.data.keys():
            if "synthetic" in request.data.keys():
                if request.data["synthetic"]:
                    # TAG-003
                    return None
                else:
                    # TAG-002
                    tag_id = request.data["tag_uuid"]
                    voices = Voice.objects.filter(created_at__lte=current_time) \
                        .filter(tag=tag_id) \
                        .order_by("-created_at")
                    serializer = VoiceSerializer(instance=voices, many=True)
                    response_json = construct_voicelist_json(list(serializer.data))
                    return Response(response_json, status=status.HTTP_200_OK)
            else:
                # tag_uuidがあるのにsyntheticがないのでエラー
                return Response(None, status.status.HTTP_400_BAD_REQUEST)
        else:
            if "synthetic" in request.data.keys():
                return Response(None, status.status.HTTP_400_BAD_REQUEST)
            else:
                # VOICE-001
                voices = Voice.objects.filter(created_at__lte=current_time) \
                    .order_by("-created_at")
                serializer = VoiceSerializer(instance=voices, many=True)
                response_json = construct_voicelist_json(list(serializer.data))
                return Response(response_json, status=status.HTTP_200_OK)


def get_sample_voice():
    """テスト用ボイス生成関数(フシギダネの鳴き声)"""
    with open("voice_sample/001.wav", "br") as f:
        b64_voice = base64.b64encode(f.read())
    return b64_voice


def construct_voicelist_json(voice_list):
    result_list = []
    for voice_dict in voice_list:
        voice = Voice.objects.get(pk=voice_dict["id"])
        tags = voice.tag.all()
        user = User.objects.filter(pk=voice_dict["created_user"])
        one_dict = {
            "user": user.values("id", "username")[0],
            "tags": list(tags.values()),
            "voice": get_sample_voice(),
            # "voice": base64.b64encode(voice_dict["voice"]),
            "like": voice_dict["like_num"],
        }
        result_list.append(one_dict)
    return {"result": result_list}


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