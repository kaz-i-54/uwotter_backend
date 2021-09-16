#from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response

from voice.models import Voice
from user.models import MyUser

# Create your views here.

class Like_historyListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        input:
        {
            'user_uuid': text,
            'voice_uuid': text
        }
        '''
        print("aaaaaaaaaaa")
        user_uuid = request.data['user_uuid']
        voice_uuid = request.data['voice_uuid']

        voice = Voice.objects.get(pk=voice_uuid)

        if not voice.filter(like__user=user_uuid).exist():
            voice.like_num += 1
            voice.save()

            like_user = MyUser.object.get(id=user_uuid)
            voice.like.add(like_user)

        return Response({'message': 'done'}, status.HTTP_201_CREATED)
