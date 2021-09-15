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
        user_uuid = request.data['user_uuid']
        tag_joined = request.data['tags']
        voice = request.data['voice']

        # new Tags
        tag_list = tag_joined.split('#')[1:]
        for tag in tag_list:
            if not Tag.objects.filter(name=tag).exists():
                newtag = Tag(name=tag)
                newtag.save()

        # new Voice
        voice_binary = base64.b64decode(voice)
        new_voice = Voice()
        # TODO now, no user search, to implement this, User DB is necessary
        new_voice.created_user = User.objects.get(username='root')
        new_voice.voice = voice_binary
        new_voice.save()
        for tag in tag_list:
            new_voice.tag.add(Tag.objects.get(name=tag))

        return Response({'message': 'done'}, status.HTTP_201_CREATED)
