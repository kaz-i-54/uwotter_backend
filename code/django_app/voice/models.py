import uuid
from django.db import models
from tag.models import Tag
from django.contrib.auth import User

# Create your models here.
class Voice(models.Model):
    class Meta:
        db_table = "voice"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice = models.BinaryField(verbose_name="ウオート")
    tag = models.ManyToManyField(Tag,verbose_name="タグ")
    like= models.ManyToManyField(User,verbose_name="いいね")
    like_num = models.IntegerField(defaut=0,verbose_name="いいね数")
    created_user = models.ForeignKey(User, verbose_name="投稿者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")
    

