# from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import VoiceSerializer
from .models import Voice
from tag.models import Tag
from django.contrib.auth.models import User

from datetime import datetime

# Create your views here.


class VoiceListAPIView(views.APIView):
    # VOICE001を実装する
    def get(self, request, *args, **kwargs):
        if "now" not in request.data.keys():
            return Response(None, status.status.HTTP_400_BAD_REQUEST)

        current_time = request.data["now"]
        print(current_time)

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


def construct_voicelist_json(voice_list):
    result_list = []
    for voice_dict in voice_list:
        voice = Voice.objects.get(pk=voice_dict["id"])
        tags = voice.tag.all()
        user = User.objects.filter(pk=voice_dict["created_user"])
        one_dict = {
            "user": user.values("id", "username")[0],
            "tags": list(tags.values()),
            "voice": "aaaaaaaaaaaaaaaa",
            # "voice": voice_dict["voice"],
            "like": voice_dict["like_num"],
        }
        result_list.append(one_dict)
    return {"result": result_list}


class VoiceCreateAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        # VOCIE002

        serializers = VoiceSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        # saved_voice = serializers.instance
        # # //あとでタグのリストをいれる
        # # //保存
        # tag_id_list = []
        # for _id in tag_id_list:
        #     saved_voice.tag.add(Tag.objects.gete(id=_id))

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
