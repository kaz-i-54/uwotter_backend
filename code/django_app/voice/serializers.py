from rest_framework import serializers
from .models import Voice


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        # fields = ["id", "voice", "like_num", "tag", "created_user"]
        fields = ["id", "voice", "like_num", "created_user"]
