# from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import User

from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag
from user.models import MyUser

from .voice_processing import multi_mixing
import base64
import json


class VoiceListAPIView(APIView):
    # VOICE001を実装する
    def get(self, request, *args, **kwargs):
        if "now" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        current_time = request.data["now"]

        if "tag_uuid" in request.data.keys():
            if "synthetic" in request.data.keys():
                if request.data["synthetic"]:
                    # TAG-003
                    tag_id = request.data["tag_uuid"]
                    voices = Voice.objects.filter(created_at__lte=current_time) \
                        .filter(tag=tag_id) \
                        .order_by("-created_at")
                    raw_voice_list = []
                    for i in voices.values("voice"):
                        raw_voice_list.append(i["voice"])
                    raw_wav_multi_data = multi_mixing(raw_voice_list)
                    response_json = construct_multivoice_json(raw_wav_multi_data, tag_id)
                    print("TAG-003 responsing...")
                    return Response(response_json, status=status.HTTP_200_OK)
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


def construct_multivoice_json(multi_wav_data, tag_id):
    tag_q = Tag.objects.filter(pk=tag_id)
    one_dict = {
        "voice": base64.b64encode(multi_wav_data),
        "tags": [tag_q.values()],
    }
    return {"result": [one_dict]}


def construct_voicelist_json(voice_list):
    result_list = []
    for voice_dict in voice_list:
        voice = Voice.objects.get(pk=voice_dict["id"])
        tags = voice.tag.all()
        user = MyUser.objects.filter(pk=voice_dict["created_user"])
        one_dict = {
            "user": user.values("id", "name")[0],
            "tags": list(tags.values()),
            # TODO: データベースからbase64にエンコード済みのデータが渡されています
            "voice": voice_dict["voice"],
            # "voice": get_sample_voice(),
            # "voice": base64.b64encode(voice_dict["voice"]),
            "like": voice_dict["like_num"],
        }
        result_list.append(one_dict)
    return {"result": result_list}


class VoiceCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        input(json):
        {
            "user_uuid": text,
            "tags": text,
            "voice": text(base64 encoded)
        }
        '''
        json_data = json.loads(request.body)
        user_uuid = json_data['user_uuid']
        tag_joined = json_data['tags']
        voice = json_data['voice']

        # new Tags
        tag_list = tag_joined.split('#')[1:]
        for tag in tag_list:
            if not Tag.objects.filter(name=tag).exists():
                newtag = Tag(name=tag)
                newtag.save()

        # new Voice
        voice_binary = base64.b64decode(voice)
        new_voice = Voice()
        new_voice.voice = voice_binary
        new_voice.created_user = MyUser.objects.get(id=user_uuid)
        new_voice.save()
        for tag in tag_list:
            new_voice.tag.add(Tag.objects.get(name=tag))

        return Response(status.HTTP_201_CREATED)
