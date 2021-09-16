#from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response

from voice.models import Voice
from user.models import MyUser


class Like_historyListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        input:
        {
            'user_uuid': text,
            'voice_uuid': text
        }
        '''
        if "user_uuid" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        if "voice_uuid" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        user_uuid = request.data['user_uuid']
        voice_uuid = request.data['voice_uuid']

        if Voice.objects.filter(id=voice_uuid).exists() is False:
            print("No such objects")
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if Voice.objects.filter(id=voice_uuid, like__id=user_uuid).exists() is False:
            # はじめてのいいねなのでインクリメント
            print("like OK")
            voice = Voice.objects.get(id=voice_uuid)
            voice.like_num += 1
            voice.save()

            user_liked = MyUser.objects.get(pk=user_uuid)
            voice.like.add(user_liked)
            voice.save()
            return Response({'message': 'done'}, status.HTTP_200_OK)
        else:
            # ほんとはインクリメントしないけどインクリメント
            print("like NOT OK")
            # voice = Voice.objects.get(id=voice_uuid)
            # voice.like_num += 1
            # voice.save()
            return Response({'message': '[future error] すでにLIKEしています'}, status.HTTP_200_OK)
