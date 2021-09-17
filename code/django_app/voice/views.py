# from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import User

from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag
from user.models import MyUser
from django.db.models import F

from .voice_processing import multi_mixing
import base64
import json
from datetime import datetime, timezone
import pytz
import re


class VoiceListAPIView(APIView):
    # VOICE001を実装する
    LIMIT_VOICE_NUM = 10

    def get(self, request, *args, **kwargs):
        current_time = request.GET.get('now', None)
        tag_uuid = request.GET.get('tag_uuid', None)
        synthetic = request.GET.get('synthetic', None)

        if current_time is not None:
            dte = datetime.strptime(current_time, "%Y/%m/%d %H:%M:%S")
            current_time = dte.replace(tzinfo=pytz.timezone("Asia/Tokyo"))

        # print(dte.ToString("%Y/%m/%d %H:%M:%S"))

        if current_time is None:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if tag_uuid is not None:
            if synthetic is not None:
                if is_uuid(tag_uuid) is False:
                    print(tag_uuid, "(tag_uuid) must be uuid format.")
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)

                if is_true(synthetic):
                    # TAG-003
                    print("-" * 20, "synthetic is called...")
                    voices = Voice.objects \
                        .filter(tag=tag_uuid) \
                        .order_by("-created_at")[:self.LIMIT_VOICE_NUM]
                    # voices = Voice.objects.filter(created_at__lte=current_time) \
                    #     .filter(tag=tag_uuid) \
                    #     .order_by("-created_at")[:self.LIMIT_VOICE_NUM]
                    if voices.exists() is False:
                        # ない場合もあるのでよくないかもしれない
                        print("該当する投稿がありません")
                        return Response({'message': '該当する投稿がありません'}, status.HTTP_400_BAD_REQUEST)
                    raw_voice_list = []
                    for i in voices.values("voice"):
                        # TODO: i["vioce"]は何があるか確認する(おそらく音声ファイルが壊れている)
                        raw_voice_list.append(i["voice"])
                    raw_wav_multi_data = multi_mixing(raw_voice_list)
                    response_json = construct_multivoice_json(raw_wav_multi_data, tag_uuid)
                    print("-" * 20, "TAG-003 responsing...")
                    return Response(response_json, status=status.HTTP_200_OK)
                elif is_false(synthetic):
                    # TAG-002
                    # voices = Voice.objects.filter(created_at__lte=current_time) \
                    #     .filter(tag=tag_uuid) \
                    #     .order_by("-created_at")[:self.LIMIT_VOICE_NUM]
                    voices = Voice.objects \
                        .filter(tag=tag_uuid) \
                        .order_by("-created_at")[:self.LIMIT_VOICE_NUM]
                    serializer = VoiceSerializer(instance=voices, many=True)
                    response_json = construct_voicelist_json(list(serializer.data))
                    return Response(response_json, status=status.HTTP_200_OK)
                else:
                    return Response(None, status.status.HTTP_400_BAD_REQUEST)
            else:
                # tag_uuidがあるのにsyntheticがないのでエラー
                return Response(None, status.status.HTTP_400_BAD_REQUEST)
        else:
            if synthetic is not None:
                return Response(None, status.status.HTTP_400_BAD_REQUEST)
            else:
                # VOICE-001
                voices = Voice.objects.order_by("-created_at")[:self.LIMIT_VOICE_NUM]
                serializer = VoiceSerializer(instance=voices, many=True)
                response_json = construct_voicelist_json(list(serializer.data))
                return Response(response_json, status=status.HTTP_200_OK)


def get_sample_voice():
    """テスト用ボイス生成関数(フシギダネの鳴き声)"""
    print("フシギダネの鳴き声をエンコード")
    with open("django_app/voice_sample/001.wav", "br") as f:
        b64_voice = base64.b64encode(f.read())
    return b64_voice


def is_true(bexp):
    if type(bexp) == str:
        return bexp.lower() in {"true"}
    return bexp


def is_false(bexp):
    if type(bexp) == str:
        return bexp.lower() in {"false"}
    return bexp


def construct_multivoice_json(multi_wav_data, tag_id):
    tag_q = Tag.objects.filter(pk=tag_id)

    # TAGのuuidの変更
    tag_list = []
    for one_tag in list(tag_q.values()):
        one_tag_dict = {
            "uuid": one_tag["id"],
            "name": one_tag["name"]
        }
        tag_list.append(one_tag_dict)
    one_dict = {
        "voice": base64.b64encode(multi_wav_data),
        # "tags": [tag_q.values()],
        "tags": tag_list
    }
    return {"result": [one_dict]}


def construct_voicelist_json(voice_list):
    result_list = []
    for voice_dict in voice_list:
        voice = Voice.objects.get(pk=voice_dict["id"])
        tags = voice.tag.all()
        user = MyUser.objects.filter(pk=voice_dict["created_user"])

        # USERのUUIDの変更
        user_dict = {
            "uuid": user.values("id")[0]["id"],
            "name": user.values("name")[0]["name"]
        }
        # TAGのuuidの変更
        tag_list = []
        for one_tag in list(tags.values()):
            one_tag_dict = {
                "uuid": one_tag["id"],
                "name": one_tag["name"]
            }
            tag_list.append(one_tag_dict)

        one_dict = {
            "uuid": voice_dict["id"],
            # "user": user.values("id", "name")[0],
            "user": user_dict,
            # "tags": list(tags.values()),
            "tags": tag_list,
            # TODO: データベースからbase64にエンコード済みのデータが渡されています
            "voice": voice_dict["voice"],
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
        if "user_uuid" not in request.data.keys() or \
                "tags" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if len(request.data["user_uuid"]) != 36:
            print("user UUID was not valid.")
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if "voice" not in request.data.keys():
            print("-" * 20, "voice can not be found")
            voice = get_sample_voice()
        else:
            voice = request.data["voice"]
            print(voice[:50])
            voice = strip_string_to_b64(voice)
            print(voice[:50])

        user_uuid = request.data['user_uuid']
        tag_joined = request.data['tags']

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


def strip_string_to_b64(text):
    text = re.sub('^data:audio/x-wav;base64,', '', text)
    return re.sub('^data:audio/wav;base64,', '', text)


def is_uuid(text):
    return len(text) == 36
