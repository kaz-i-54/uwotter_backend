from .models import Tag
from rest_framework import serializers


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        # read_only_fields = ()

    """
    def get_full_name(self, instance):
        return instance.get_full_name()  # User に元からあるメソッドを呼び出してるだけ

    def create(self, validated_data):
        password = validated_data.pop('password', 'something')  # そのまま使っちゃだめだよ
        user = User(username=uuid.uuid4().hex, password=make_password(password), **validated_data)
        user.save()
        return user
    """
