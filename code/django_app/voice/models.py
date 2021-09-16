import uuid
from django.db import models
from tag.models import Tag
from django.contrib.auth.models import User

# Create your models here.


class Voice(models.Model):
    class Meta:
        db_table = "voice"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice = models.BinaryField(verbose_name="ウオート", null=False)
    like_num = models.IntegerField(default=0, verbose_name="いいね数")
    created_user = models.OneToOneField(User, verbose_name="投稿者", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")

    like = models.ManyToManyField(User, verbose_name="いいね", related_name="like_people") 
    tag = models.ManyToManyField(Tag, verbose_name="タグ")
