import uuid
from django.db import models
from tag.models import Tag
# from django.contrib.auth.models import User
from user.models import MyUser
from django.utils import timezone

# Create your models here.


class Voice(models.Model):
    class Meta:
        db_table = "voice"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice = models.BinaryField(verbose_name="ウオート", null=False)
    like_num = models.IntegerField(default=0, verbose_name="いいね数")
    created_user = models.ForeignKey(MyUser, verbose_name="投稿者", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="投稿日時")

    like = models.ManyToManyField(MyUser, verbose_name="いいね", related_name="like_people")
    tag = models.ManyToManyField(Tag, verbose_name="タグ")

    def __str__(self):
        return str(self.created_at)
